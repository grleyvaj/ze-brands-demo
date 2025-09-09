from fastapi import FastAPI

from app.openapi import openapi


def test_when_openapi_is_load_then_documentation_is_built():
    app = FastAPI(redoc_url="/")
    app.openapi_schema = {
        "title": "Categorization - Machine Learning",
        "version": "1.2.0",
        "description": "Get your transactions categorized",
        "routes": app.routes,
    }

    current = openapi(app)

    assert current["title"] == "Categorization - Machine Learning"
    assert current["version"] == "1.2.0"
    assert current["description"] == "Get your transactions categorized"
