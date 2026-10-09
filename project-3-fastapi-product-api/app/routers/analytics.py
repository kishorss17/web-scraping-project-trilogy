"""
Analytics & Aggregations Router
Uses MongoDB Aggregation Pipelines to serve catalog intelligence and metrics.
"""
from typing import List
from fastapi import APIRouter, Depends, Query
from motor.motor_asyncio import AsyncIOMotorCollection

from app.dependencies import get_products_col
from app.models import (
    AnalyticsOverview,
    CategoryStat,
    PriceDistributionBucket,
    ProductResponse
)
from app.utils.helpers import normalize_product_doc

router = APIRouter(prefix="/api/v1/analytics", tags=["Catalog Analytics"])


@router.get(
    "/overview",
    response_model=AnalyticsOverview,
    summary="Get catalog-wide summary statistics",
    description="Aggregates catalog metrics including average price, price range, average rating, and inventory stock breakdown."
)
async def get_catalog_overview(
    col: AsyncIOMotorCollection = Depends(get_products_col)
):
    pipeline = [
        {
            "$facet": {
                "general_stats": [
                    {
                        "$group": {
                            "_id": None,
                            "total": {"$sum": 1},
                            "avg_price": {"$avg": "$price"},
                            "min_price": {"$min": "$price"},
                            "max_price": {"$max": "$price"},
                            "avg_rating": {"$avg": "$rating"}
                        }
                    }
                ],
                "in_stock": [
                    {
                        "$match": {
                            "availability": {"$regex": "in stock", "$options": "i"}
                        }
                    },
                    {"$count": "count"}
                ],
                "categories": [
                    {
                        "$group": {
                            "_id": "$category"
                        }
                    },
                    {"$count": "count"}
                ]
            }
        }
    ]

    result = await col.aggregate(pipeline).to_list(length=1)

    if not result or not result[0]["general_stats"]:
        # Fallback if catalog is empty
        total_docs = await col.count_documents({})
        return AnalyticsOverview(
            total_products=total_docs,
            avg_price=0.0,
            min_price=0.0,
            max_price=0.0,
            avg_rating=0.0,
            in_stock_count=0,
            out_of_stock_count=0,
            total_categories=0
        )

    stats = result[0]["general_stats"][0]
    total = stats.get("total", 0)
    in_stock = result[0]["in_stock"][0]["count"] if result[0]["in_stock"] else 0
    categories_count = result[0]["categories"][0]["count"] if result[0]["categories"] else 0
    out_of_stock = max(0, total - in_stock)

    return AnalyticsOverview(
        total_products=total,
        avg_price=round(float(stats.get("avg_price", 0.0) or 0.0), 2),
        min_price=round(float(stats.get("min_price", 0.0) or 0.0), 2),
        max_price=round(float(stats.get("max_price", 0.0) or 0.0), 2),
        avg_rating=round(float(stats.get("avg_rating", 0.0) or 0.0), 2),
        in_stock_count=in_stock,
        out_of_stock_count=out_of_stock,
        total_categories=categories_count
    )


@router.get(
    "/categories",
    response_model=List[CategoryStat],
    summary="Get aggregated statistics per category",
    description="Groups catalog by category to compute product count, average price, price extremes, and mean rating."
)
async def get_category_analytics(
    min_count: int = Query(1, ge=1, description="Minimum product count in category to include"),
    limit: int = Query(50, ge=1, le=100, description="Max categories to return"),
    col: AsyncIOMotorCollection = Depends(get_products_col)
):
    pipeline = [
        {
            "$group": {
                "_id": {"$ifNull": ["$category", "Uncategorized"]},
                "count": {"$sum": 1},
                "avg_price": {"$avg": "$price"},
                "min_price": {"$min": "$price"},
                "max_price": {"$max": "$price"},
                "avg_rating": {"$avg": "$rating"}
            }
        },
        {"$match": {"count": {"$gte": min_count}}},
        {"$sort": {"count": -1, "avg_price": -1}},
        {"$limit": limit}
    ]

    cursor = col.aggregate(pipeline)
    raw_results = await cursor.to_list(length=limit)

    return [
        CategoryStat(
            category=str(item["_id"]),
            count=item["count"],
            avg_price=round(float(item.get("avg_price", 0.0) or 0.0), 2),
            min_price=round(float(item.get("min_price", 0.0) or 0.0), 2),
            max_price=round(float(item.get("max_price", 0.0) or 0.0), 2),
            avg_rating=round(float(item.get("avg_rating", 0.0) or 0.0), 2)
        )
        for item in raw_results
    ]


@router.get(
    "/price-distribution",
    response_model=List[PriceDistributionBucket],
    summary="Get product distribution across price brackets",
    description="Buckets products into price tiers (Budget <£20, Mid £20-£40, Premium £40-£60, Luxury £60+) with percentages."
)
async def get_price_distribution(
    col: AsyncIOMotorCollection = Depends(get_products_col)
):
    total_docs = await col.count_documents({})
    if total_docs == 0:
        return []

    pipeline = [
        {
            "$facet": {
                "under_20": [
                    {"$match": {"price": {"$lt": 20.0}}},
                    {"$count": "count"}
                ],
                "20_to_40": [
                    {"$match": {"price": {"$gte": 20.0, "$lt": 40.0}}},
                    {"$count": "count"}
                ],
                "40_to_60": [
                    {"$match": {"price": {"$gte": 40.0, "$lt": 60.0}}},
                    {"$count": "count"}
                ],
                "60_plus": [
                    {"$match": {"price": {"$gte": 60.0}}},
                    {"$count": "count"}
                ]
            }
        }
    ]

    res = await col.aggregate(pipeline).to_list(length=1)
    if not res:
        return []

    facet_data = res[0]
    buckets = [
        ("Budget (Under £20)", 0.0, 20.0, facet_data.get("under_20")),
        ("Mid-Tier (£20 - £40)", 20.0, 40.0, facet_data.get("20_to_40")),
        ("Premium (£40 - £60)", 40.0, 60.0, facet_data.get("40_to_60")),
        ("Luxury (£60+)", 60.0, None, facet_data.get("60_plus")),
    ]

    results = []
    for label, min_p, max_p, data in buckets:
        cnt = data[0]["count"] if data else 0
        pct = round((cnt / total_docs) * 100, 2)
        results.append(PriceDistributionBucket(
            label=label,
            min_price=min_p,
            max_price=max_p,
            count=cnt,
            percentage=pct
        ))

    return results


@router.get(
    "/top-rated",
    response_model=List[ProductResponse],
    summary="Get highest rated products",
    description="Retrieve the top rated products in catalog, sorted by rating descending then price ascending."
)
async def get_top_rated_products(
    limit: int = Query(10, ge=1, le=50, description="Number of products to return"),
    col: AsyncIOMotorCollection = Depends(get_products_col)
):
    cursor = col.find().sort([("rating", -1), ("price", 1)]).limit(limit)
    docs = await cursor.to_list(length=limit)
    return [ProductResponse(**normalize_product_doc(doc)) for doc in docs]
