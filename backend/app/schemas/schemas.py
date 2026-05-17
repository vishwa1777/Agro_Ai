from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field


# ─── Auth ─────────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    employee_id: str
    territory: str = ""
    territory_id: str = ""
    role: str = "field_agent"
    region_id: str = "br"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    employee_id: str
    role: str
    territory: str
    territory_id: str
    region_id: str
    theme: str
    language: str
    notifications: Dict[str, bool]
    sync_enabled: bool


# ─── Dashboard ────────────────────────────────────────────────────────────────

class KPIResponse(BaseModel):
    id: str
    title: str
    value: str
    trend: str
    trend_direction: str
    icon: str
    icon_color: str
    icon_bg: str
    chart_data: List[float]
    chart_color: str


class WeeklyPerformancePoint(BaseModel):
    name: str
    value: float   # visits completed
    value2: float  # target
    value3: float  # actual revenue (Lakhs)


class DashboardResponse(BaseModel):
    kpis: List[KPIResponse]
    weekly_performance: List[WeeklyPerformancePoint]
    notifications_count: int


# ─── Recommendations ──────────────────────────────────────────────────────────

class ExplainableReason(BaseModel):
    id: str
    title: str
    description: str
    icon: str


class RecommendationResponse(BaseModel):
    id: str
    priority: str
    crop: str
    message: str
    weather: str
    product: str
    village: str
    farmer: Optional[str] = None
    pest_risk: Optional[str] = None
    next_action: Optional[str] = None
    follow_up_timeline: Optional[List[str]] = None
    explainable_reasons: Optional[List[ExplainableReason]] = None
    retailer_id: Optional[str] = None
    visit_priority_score: Optional[float] = None


class ApplyRecommendationRequest(BaseModel):
    recommendation_id: str
    retailer_id: str
    action: str = "apply"  # apply | dismiss


# ─── Visit Planner ────────────────────────────────────────────────────────────

class VisitTag(BaseModel):
    label: str
    color: str  # green | blue | red | yellow


class PriorityVisitResponse(BaseModel):
    id: str
    name: str
    type: str  # retailer | village | cluster
    score: float
    location: str
    last_visit: str
    status: str
    tags: List[VisitTag]
    ai_reason: str
    actions: List[str]
    retailer_id: str
    lat: Optional[float] = None
    lng: Optional[float] = None


class RouteStop(BaseModel):
    id: int
    name: str
    lat: float
    lng: float
    status: str  # completed | in-progress | pending
    time: str
    retailer_id: str


class RouteResponse(BaseModel):
    stops: List[RouteStop]
    total_distance_km: float
    estimated_hours: float
    total_stops: int


class VisitActionRequest(BaseModel):
    retailer_id: str
    action: str  # start | complete | reschedule | skip
    notes: str = ""
    revenue_generated: float = 0
    products_discussed: List[str] = []


class VisitActionResponse(BaseModel):
    success: bool
    message: str
    visit_id: Optional[str] = None


# ─── ML Prediction ────────────────────────────────────────────────────────────

class PredictRequest(BaseModel):
    sales_qty_30: float = 0
    sales_value_30: float = 0
    transactions_30: float = 0
    sales_qty_7: float = 0
    sales_value_7: float = 0
    transactions_7: float = 0
    sales_growth_ratio: float = 0
    total_stock_qty: float = 0
    unique_skus: float = 0
    last_visit_days: float = 0
    product_sales_qty_30: float = 0
    grower_count: float = 0
    avg_farm_size: float = 0
    product_scans: float = 0
    campaign_attendance: float = 0
    total_messages: float = 0
    total_opened: float = 0
    total_clicked: float = 0
    engagement_rate: float = 0


class PredictResponse(BaseModel):
    visit_priority_score: float
    priority_level: str  # High | Medium | Low
    action_type: str     # urgent | planned | monitor
    explanation: str


# ─── Risk Analyzer ────────────────────────────────────────────────────────────

class NDVIDataPoint(BaseModel):
    date: str
    healthy: float
    moderate: float
    stressed: float


class HeatmapCell(BaseModel):
    id: int
    x: int
    y: int
    risk: str  # low | medium | high | critical
    village: str
    risk_percent: float


class PestOutbreak(BaseModel):
    id: int
    lat: float
    lng: float
    pest: str
    severity: str  # Medium | High | Critical
    crop: str
    village: str


class WeatherAnomaly(BaseModel):
    id: int
    lat: float
    lng: float
    type: str  # rain | drought | wind
    label: str
    temp: str
    condition: str


class RiskAnalyzerResponse(BaseModel):
    heatmap: List[HeatmapCell]
    ndvi_data: List[NDVIDataPoint]
    pest_outbreaks: List[PestOutbreak]
    weather_anomalies: List[WeatherAnomaly]
    overall_risk_level: str
    ai_insights: List[str]


# ─── Analytics ────────────────────────────────────────────────────────────────

class ChartDataPoint(BaseModel):
    name: str
    value: float
    value2: Optional[float] = None


class CropRiskTrend(BaseModel):
    month: str
    rice: float
    cotton: float
    wheat: float


class StockItem(BaseModel):
    product: str
    utilization: float
    stock: int
    status: str  # optimal | low | critical


class RegionalPerformance(BaseModel):
    metric: str
    your_territory: float
    average: float


class AnalyticsResponse(BaseModel):
    field_efficiency: List[ChartDataPoint]
    revenue_per_visit: List[ChartDataPoint]
    recommendation_acceptance: List[Dict[str, Any]]
    regional_performance: List[RegionalPerformance]
    crop_risk_trends: List[CropRiskTrend]
    stock_utilization: List[StockItem]


# ─── Mandi ────────────────────────────────────────────────────────────────────

class MandiPriceResponse(BaseModel):
    crop: str
    icon: str
    price: str
    unit: str
    change: str
    up: bool
    market: str
    updated_at: str


# ─── AI Chat ──────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    session_id: str
    region: str = "Bihar"


class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: str


# ─── Settings ─────────────────────────────────────────────────────────────────

class UpdateSettingsRequest(BaseModel):
    theme: Optional[str] = None
    language: Optional[str] = None
    notifications: Optional[Dict[str, bool]] = None
    sync_enabled: Optional[bool] = None
    region_id: Optional[str] = None


class UpdateSettingsResponse(BaseModel):
    success: bool
    message: str
    updated: Dict[str, Any]
