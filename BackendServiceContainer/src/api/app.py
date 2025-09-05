from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, transactions, reports, health
from .core.docs import openapi_tags, api_description

def create_app() -> FastAPI:
    """
    Factory to create and configure the FastAPI application.
    """
    app = FastAPI(
        title="Ledger Management Backend Service API",
        version="1.0.0",
        description=api_description,
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.openapi_tags = openapi_tags

    # Routers
    app.include_router(health.router, prefix="", tags=["Health"])
    app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
    app.include_router(transactions.router, prefix="/transactions", tags=["Transactions"])
    app.include_router(reports.router, prefix="/reports", tags=["Reports"])

    return app

app = create_app()
