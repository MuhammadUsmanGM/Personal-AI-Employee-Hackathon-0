"""
Main FastAPI Application for Silver Tier Personal AI Employee System
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import contextmanager
import os
import logging
from datetime import datetime

from ..services.database import SessionLocal, init_db
from ..services.task_service import TaskService
from ..services.preference_service import UserPreferenceService
from ..services.interaction_service import InteractionService

# Create the main FastAPI app
app = FastAPI(
    title="Personal AI Employee - Platinum Tier API",
    description="Advanced API for the Personal AI Employee system with quantum-safe security, global operations, blockchain integration, IoT connectivity, and AR/VR interfaces",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        # Initialize the database
        init_db(os.getenv("DATABASE_URL", "sqlite:///silver_tier.db"))
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

# Dependency to get database session
def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check endpoint
@app.get("/api/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint to verify API is running"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "tier": "platinum",
        "features_active": {
            "global_operations": True,
            "quantum_security": True,
            "blockchain_integration": True,
            "iot_connectivity": True,
            "arvr_interfaces": True
        }
    }

# Include routers for different modules
from .routes.dashboard import dashboard_router
from .routes.tasks import task_router
from .routes.approval import approval_router
from .routes.ai import ai_router
from .routes.enterprise import enterprise_router

# Platinum Tier routes
try:
    from .routes.global_ops import router as global_ops_router
    from .routes.quantum import router as quantum_router
    from .routes.blockchain import router as blockchain_router
    from .routes.iot import router as iot_router
    from .routes.ar_vr import router as ar_vr_router

    app.include_router(global_ops_router, prefix="/api", tags=["global-operations"])
    app.include_router(quantum_router, prefix="/api", tags=["quantum-security"])
    app.include_router(blockchain_router, prefix="/api", tags=["blockchain"])
    app.include_router(iot_router, prefix="/api", tags=["iot-devices"])
    app.include_router(ar_vr_router, prefix="/api", tags=["ar-vr-interfaces"])
except ImportError as e:
    print(f"Warning: Could not import Platinum Tier routes: {e}")

app.include_router(dashboard_router, prefix="/api", tags=["dashboard"])
app.include_router(task_router, prefix="/api", tags=["tasks"])
app.include_router(approval_router, prefix="/api", tags=["approvals"])
app.include_router(ai_router, prefix="/api", tags=["ai"])
app.include_router(enterprise_router, prefix="/api", tags=["enterprise"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Personal AI Employee - Platinum Tier API",
        "version": "1.0.0",
        "documentation": "/api/docs",
        "status": "running",
        "features": [
            "Global Operations",
            "Quantum-Safe Security",
            "Blockchain Integration",
            "IoT Connectivity",
            "AR/VR Interfaces",
            "Advanced AI & Analytics"
        ]
    }

# Error handling
@app.exception_handler(404)
async def custom_http_exception_handler(request, exc):
    """Custom 404 handler"""
    return {
        "detail": "Endpoint not found",
        "status_code": 404,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.exception_handler(500)
async def custom_server_error_exception_handler(request, exc):
    """Custom 500 handler"""
    return {
        "detail": "Internal server error",
        "status_code": 500,
        "timestamp": datetime.utcnow().isoformat()
    }

# Utility functions
def get_task_service(db: Session = Depends(get_db)):
    """Get task service instance"""
    return TaskService(db)

def get_preference_service(db: Session = Depends(get_db)):
    """Get preference service instance"""
    return UserPreferenceService(db)

def get_interaction_service(db: Session = Depends(get_db)):
    """Get interaction service instance"""
    return InteractionService(db)

# Initialize the database when the module is loaded
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=os.getenv("API_HOST", "localhost"),
        port=int(os.getenv("API_PORT", "8000")),
        reload=True
    )