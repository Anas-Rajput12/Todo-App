from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .api.auth import router as auth_router
from .api.tasks import router as tasks_router
from .middleware.auth import JWTBearer
from .database import engine
from . import models  # Import models for table creation
from sqlmodel import SQLModel


def create_app():
    app = FastAPI(
        title="Todo Web App API",
        description="API for managing user tasks in the Todo Web App",
        version="1.0.0",
        # Add security headers
        root_path=""  # Adjust if behind proxy
    )

    # Rate limiter
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Add security-related middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allow all origins for development/deployment
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # In production, be more restrictive:
        # allow_origins=["https://yourdomain.com"],
    )

    # Additional middleware to handle potential CORS issues
    @app.middleware("http")
    async def add_cors_headers(request, call_next):
        response = await call_next(request)
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "*"
        return response

    # Add GZip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Trusted Host Middleware - only allow requests from specific hosts
    # In production, replace with your actual domain
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

    # Include routers
    app.include_router(auth_router, prefix="/v1/auth", tags=["Authentication"])
    app.include_router(tasks_router, prefix="/v1/tasks", tags=["Tasks"])

    # Create database tables
    SQLModel.metadata.create_all(bind=engine)

    # Add security headers to all responses
    @app.middleware("http")
    async def add_security_headers(request, call_next):
        response = await call_next(request)

        # Set security headers (be more permissive for deployment environments)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"  # Changed from DENY to SAMEORIGIN for deployment
        response.headers["X-XSS-Protection"] = "1; mode=block"
        # Comment out HSTS for deployment environment to avoid HTTPS issues
        # response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        return response

    return app


app = create_app()


@app.get("/")
def read_root():
    return {"message": "Welcome to Todo Web App API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Add the standard Python entry point for running the server
if __name__ == "__main__":
    import uvicorn
    import os

    # Get host and port from environment variables or use defaults
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", 8000))

    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload for development
        debug=os.getenv("DEBUG", "false").lower() == "true"
    )