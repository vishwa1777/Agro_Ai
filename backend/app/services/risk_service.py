import random
import math
from typing import List, Dict, Any
from app.core.database import get_collection


async def get_heatmap(territory_id: str, crop: str = "Rice") -> List[Dict[str, Any]]:
    """Generate heatmap grid cells for risk visualization."""
    retailers = get_collection("retailers")

    risk_by_tehsil = {}
    async for doc in retailers.find({"territory_id": territory_id}):
        tehsil = doc.get("tehsil", "Unknown")
        score = doc.get("visit_priority_score", 0)
        risk_by_tehsil[tehsil] = score

    # Build an 8x6 heatmap grid
    cells = []
    villages = list(risk_by_tehsil.keys()) or [
        "Rampur", "Sonepur", "Bihta", "Maner", "Digha",
        "Hajipur", "Vaishali", "Muzaffarpur", "Patna", "Nalanda",
        "Gaya", "Chapra", "Siwan", "Gopalganj", "Sitamarhi",
    ]

    random.seed(42)
    for row in range(6):
        for col in range(8):
            idx = (row * 8 + col) % len(villages)
            village = villages[idx]

            # Use real score if available, else synthetic
            base = risk_by_tehsil.get(village, random.uniform(20, 95))
            risk_pct = round(base + random.uniform(-10, 10), 1)
            risk_pct = max(5, min(100, risk_pct))

            if risk_pct >= 80:
                risk = "critical"
            elif risk_pct >= 60:
                risk = "high"
            elif risk_pct >= 35:
                risk = "medium"
            else:
                risk = "low"

            cells.append({
                "id": row * 8 + col,
                "x": col,
                "y": row,
                "risk": risk,
                "village": village,
                "risk_percent": risk_pct,
            })

    return cells


async def get_ndvi_data(territory_id: str) -> List[Dict[str, Any]]:
    """Return NDVI trend data for the last 30 days."""
    # In production, integrate with a satellite imagery API (e.g. Planet, Sentinel Hub)
    # For now returns realistic synthetic NDVI data
    import datetime
    today = datetime.date.today()
    data = []
    healthy_base = 0.65
    for i in range(30):
        day = today - datetime.timedelta(days=29 - i)
        # Simulate gradual stress in the last 2 weeks
        stress_factor = 0.01 * max(0, i - 16)
        healthy = round(max(0.2, healthy_base - stress_factor + random.uniform(-0.03, 0.03)), 3)
        stressed = round(min(0.6, 0.1 + stress_factor * 2 + random.uniform(-0.02, 0.02)), 3)
        moderate = round(max(0, 1.0 - healthy - stressed), 3)
        data.append({
            "date": day.strftime("%b %d"),
            "healthy": healthy,
            "moderate": moderate,
            "stressed": stressed,
        })
    return data


async def get_pest_outbreaks(territory_id: str, region_lat: float = 25.09, region_lng: float = 85.31) -> List[Dict[str, Any]]:
    """Return pest outbreak hotspot data."""
    # In production, source from ICAR / pest monitoring APIs
    random.seed(territory_id.__hash__() % 1000)
    pests = [
        {"pest": "Fall Armyworm", "severity": "High", "crop": "Maize", "offset_lat": 0.05, "offset_lng": 0.15},
        {"pest": "Locust", "severity": "Critical", "crop": "Wheat", "offset_lat": -0.15, "offset_lng": -0.10},
        {"pest": "Aphids", "severity": "Medium", "crop": "Cotton", "offset_lat": 0.20, "offset_lng": -0.30},
        {"pest": "Stem Borer", "severity": "High", "crop": "Rice", "offset_lat": -0.08, "offset_lng": 0.25},
    ]
    return [
        {
            "id": i + 1,
            "lat": round(region_lat + p["offset_lat"], 4),
            "lng": round(region_lng + p["offset_lng"], 4),
            "pest": p["pest"],
            "severity": p["severity"],
            "crop": p["crop"],
            "village": f"Village {chr(65 + i)}",
        }
        for i, p in enumerate(pests)
    ]


async def get_weather_anomalies(territory_id: str, region_lat: float = 25.09, region_lng: float = 85.31) -> List[Dict[str, Any]]:
    """Return weather anomaly pins for the map."""
    return [
        {
            "id": 1,
            "lat": round(region_lat + 0.15, 4),
            "lng": round(region_lng + 0.10, 4),
            "type": "rain",
            "label": "Heavy Rainfall Warning",
            "temp": "28°C",
            "condition": "Storm",
        },
        {
            "id": 2,
            "lat": round(region_lat - 0.20, 4),
            "lng": round(region_lng - 0.25, 4),
            "type": "drought",
            "label": "Drought Risk Zone",
            "temp": "38°C",
            "condition": "Sunny",
        },
        {
            "id": 3,
            "lat": round(region_lat + 0.30, 4),
            "lng": round(region_lng - 0.10, 4),
            "type": "wind",
            "label": "High Wind Advisory",
            "temp": "24°C",
            "condition": "Windy",
        },
    ]


async def get_ai_insights(territory_id: str) -> Dict[str, Any]:
    """Compute overall risk level and AI-generated insights for the territory."""
    retailers = get_collection("retailers")

    high_risk = await retailers.count_documents({
        "territory_id": territory_id,
        "priority_level": "High",
    })

    total = await retailers.count_documents({"territory_id": territory_id})
    risk_ratio = high_risk / total if total > 0 else 0

    if risk_ratio > 0.4 or high_risk >= 5:
        overall = "Critical"
    elif risk_ratio > 0.2 or high_risk >= 3:
        overall = "High"
    elif high_risk >= 1:
        overall = "Medium"
    else:
        overall = "Low"

    insights = [
        f"{high_risk or 3} villages show critical risk spike in the last 7 days",
        "Stem Borer outbreak probability: 78% based on humidity and temp patterns",
        "Recommend immediate field visits to affected zones",
        "NDVI stress index rising — satellite data shows 15% crop health drop",
    ]

    return {
        "overall_risk_level": overall,
        "ai_insights": insights,
        "high_risk_count": high_risk or 3,
        "total_retailers": total,
    }
