from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.core.configurations import settings


def openapi(app: FastAPI) -> dict:
    if app.openapi_schema:
        return app.openapi_schema

    dev_port = settings.DEV_PORT

    openapi_schema = get_openapi(
        title="ZeBrands Catalog API",
        version="1.0.0",
        description="API for manage catalog of products and users",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        },
    }

    openapi_schema["info"].update(
        {
            "contact": {
                "name": "ZeBrands Support",
                "url": "https://github.com/grleyvaj",
                "email": "support@zebrands.com",
            },
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT",
            },
            "termsOfService": "https://zebrands.com/terms",
        },
    )

    openapi_schema["servers"] = [
        {"url": f"http://localhost:{dev_port}", "description": "Development server"},
        {"url": "https://uat.api.zebrands.com", "description": "UAT server"},
        {"url": "https://api.zebrands.com", "description": "Production server"},
    ]

    openapi_schema["tags"] = [
        {"name": "Access", "description": "Manage access"},
        {"name": "Users", "description": "Operations with users"},
        {"name": "Brands", "description": "Operations with brands"},
        {"name": "Products", "description": "Operations with products"},
    ]

    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"bearerAuth": []})

    app.openapi_schema = openapi_schema

    return app.openapi_schema
