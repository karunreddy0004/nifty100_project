from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import time

from src.api.routers import health
from src.api.routers import companies
from src.api.routers import documents
from src.api.routers import screener
from src.api.routers import peers
from src.api.routers import sectors
from src.api.routers import portfolio
from src.api.routers import valuation
from src.api.routers import risk
from src.api.routers import investment_scores
from src.api.routers import investor_reports
from src.api.routers import company_summary
from src.api.routers import dashboard
from src.api.routers import stock_prices
from src.api.routers import analytics
# ---------------------------------------------------
# Swagger Tags
# ---------------------------------------------------

tags_metadata = [
    {
        "name": "Health",
        "description": "Health check endpoints."
    },
    {
        "name": "Companies",
        "description": "Company information and financial statements."
    },
    {
        "name": "Documents",
        "description": "Company annual reports and documents."
    },
    {
        "name": "Screener",
        "description": "Stock screener with multiple filters."
    },
    {
        "name": "Peers",
        "description": "Peer group comparison."
    },
    {
        "name": "Sectors",
        "description": "Sector-wise information."
    },
    {
        "name": "Portfolio",
        "description": "Portfolio recommendations."
    },
    {
        "name": "Valuation",
        "description": "Company valuation analysis."
    },
    {
        "name": "Risk",
        "description": "Company risk analysis."
    },
    {
        "name": "Investment Scores",
        "description": "Investment score and ratings."
    },
    {
        "name": "Investor Reports",
        "description": "Generated investor reports."
    },
    {
        "name": "Company Summary",
        "description": "Company summaries."
    },
    {
        "name": "Dashboard",
        "description": "Dashboard analytics."
    },
    {
        "name": "Stock Prices",
        "description": "Historical stock prices."
    },
    {
        "name": "Analytics",
        "description": "Overall project analytics."
    }
]

app = FastAPI(
    title="Nifty100 Investment Analytics API",
    description="REST API for Nifty100 Financial Analytics Dashboard",
    version="1.0.0",
    contact={
        "name": "Karun Reddy",
        "email": "your_email@example.com"
    },
    license_info={
        "name": "MIT"
    },
    openapi_tags=tags_metadata
)
# ---------------------------------------------------
# CORS
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# Request Logging Middleware
# ---------------------------------------------------

@app.middleware("http")
async def request_logger(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = time.time() - start

    print(
        f"{request.method} {request.url.path} {duration:.4f}s"
    )

    return response


# ---------------------------------------------------
# API Routers
# ---------------------------------------------------

app.include_router(
    health.router,
    prefix="/api/v1",
)

app.include_router(
    companies.router,
    prefix="/api/v1"
)
app.include_router(
    documents.router,
    prefix="/api/v1"
)
app.include_router(
    screener.router,
    prefix="/api/v1"
)
app.include_router(
    peers.router,
    prefix="/api/v1"
)
app.include_router(
    sectors.router,
    prefix="/api/v1"
)
app.include_router(
    portfolio.router,
    prefix="/api/v1"
)
app.include_router(
    valuation.router,
    prefix="/api/v1"
)
app.include_router(
    risk.router,
    prefix="/api/v1"
)
app.include_router(
    investment_scores.router,
    prefix="/api/v1"
)
app.include_router(
    investor_reports.router,
    prefix="/api/v1"
)
app.include_router(
    company_summary.router,
    prefix="/api/v1"
)
app.include_router(
    dashboard.router,
    prefix="/api/v1"
)
app.include_router(
    stock_prices.router,
    prefix="/api/v1"
)
app.include_router(
    analytics.router,
    prefix="/api/v1"
)

# ---------------------------------------------------
# Root Endpoint
# ---------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Nifty100 Investment Intelligence API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
    }