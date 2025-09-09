from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from app.application.api.products.create.mappers import ProductCreateInputMapper
from app.application.api.products.create.schemas import ProductCreateRequest
from app.application.api.products.detail.mappers import ProductDetailResponseMapper
from app.application.api.products.detail.schemas import ProductDetailResponse
from app.application.api.products.edit.mappers import ProductUpdateInputMapper
from app.application.api.products.edit.schemas import ProductUpdateRequest
from app.application.api.products.list.schemas import (
    ProductListItemResponse,
    ProductListResponse,
)
from app.application.containers import container
from app.core.role_checker import RoleChecker
from app.domain.enums.role_enum import UserRole
from app.domain.use_cases.products.create.product_create_use_case import (
    ProductCreateUseCase,
)
from app.domain.use_cases.products.detail.product_detail_use_case import (
    ProductDetailUseCase,
)
from app.domain.use_cases.products.edit.product_update_use_case import (
    ProductUpdateUseCase,
)
from app.domain.use_cases.products.remove.product_remove_use_case import (
    ProductRemoveUseCase,
)
from app.domain.use_cases.products.view_report.product_view_report_use_case import (
    ProductViewReportUseCase,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    dependencies=[Depends(RoleChecker(["ADMIN"]))],
    summary="Create a new product",
    description=(
        "Creates a new product in the catalog. Validates that the SKU is unique. "
        "Accessible by only admins."
    ),
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["sku"],
                                "msg": "Product with SKU '123' already exists",
                                "type": "ALREADY_EXIST_PRODUCT_SKU",
                            },
                        ],
                    },
                },
            },
        },
        status.HTTP_403_FORBIDDEN: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You do not have permission to perform this action",
                    },
                },
            },
        },
    },
)
def create_product(
    request: ProductCreateRequest,
    use_case: Annotated[
        ProductCreateUseCase,
        Depends(lambda: container.resolve(ProductCreateUseCase)),
    ],
) -> ProductDetailResponse:
    product = use_case.create_product(
        create_input=ProductCreateInputMapper.map(request),
    )

    return ProductDetailResponseMapper.map(product)


@router.get(
    "/views",
    dependencies=[Depends(RoleChecker(["ADMIN", "ANONYMOUS"]))],
    summary="Views of products",
    description="Returns a list of products's views. Optionally filter by brand_id. "
    "Includes view counts.",
    responses={
        status.HTTP_403_FORBIDDEN: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You do not have permission to perform this action",
                    },
                },
            },
        },
    },
)
def views_report(
    use_case: Annotated[
        ProductViewReportUseCase,
        Depends(lambda: container.resolve(ProductViewReportUseCase)),
    ],
    brand_id: Annotated[
        str | None,
        Query(
            title="Brand ID",
            description="Filter products by brand ID",
            examples=["01K4EH5T4YQERHJ99RM1SWYV99"],
        ),
    ] = None,
) -> ProductListResponse:
    product_views = use_case.view_report(brand_id=brand_id)
    return ProductListResponse(
        products=[
            ProductListItemResponse(
                id=product.id,
                name=product.name,
                views=product.view,
            )
            for product in product_views
        ],
    )


@router.get(
    "/{product_id}",
    dependencies=[Depends(RoleChecker(["ADMIN", "ANONYMOUS"]))],
    summary="Get product details",
    description=(
        "Retrieves the details of a product by its ID. "
        "Accessible by anonymous users or admins."
    ),
    responses={
        status.HTTP_403_FORBIDDEN: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You do not have permission to perform this action",
                    },
                },
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Product not found",
                    },
                },
            },
        },
    },
)
def get_product(
    use_case: Annotated[
        ProductDetailUseCase,
        Depends(lambda: container.resolve(ProductDetailUseCase)),
    ],
    product_id: Annotated[
        str,
        Path(
            ...,
            description="Product identifier in ULID format",
            examples=["01K4EH5T4YQERHJ99RM1SWYV99"],
        ),
    ],
    user: Annotated[dict, Depends(RoleChecker(["ADMIN", "ANONYMOUS"]))],
) -> ProductDetailResponse:
    increment_view = user.get("role") == UserRole.ANONYMOUS.value
    product = use_case.get_product(product_id=product_id, increment_view=increment_view)
    return ProductDetailResponseMapper.map(product)


@router.put(
    "/{product_id}",
    dependencies=[Depends(RoleChecker(["ADMIN"]))],
    summary="Update an existing product",
    description="Updates the fields of an existing product. "
    "Only admins can perform this action.",
    responses={
        status.HTTP_403_FORBIDDEN: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You do not have permission to perform this action",
                    },
                },
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "example": {"detail": "Product not found"},
                },
            },
        },
    },
)
def update_product(
    use_case: Annotated[
        ProductUpdateUseCase,
        Depends(lambda: container.resolve(ProductUpdateUseCase)),
    ],
    request: ProductUpdateRequest,
    product_id: Annotated[
        str,
        Path(
            ...,
            description="Product identifier in ULID format",
            examples=["01K4EH5T4YQERHJ99RM1SWYV99"],
        ),
    ],
) -> ProductDetailResponse:
    updated_product = use_case.update_product(
        product_id=product_id,
        update_input=ProductUpdateInputMapper.map(request),
    )
    return ProductDetailResponseMapper.map(updated_product)


@router.delete(
    "/{product_id}",
    dependencies=[Depends(RoleChecker(["ADMIN"]))],
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product",
    description="Deletes a product by ID. Only admins can perform this action.",
    responses={
        status.HTTP_403_FORBIDDEN: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": "You do not have permission to perform this action",
                    },
                },
            },
        },
    },
)
def delete_product(
    use_case: Annotated[
        ProductRemoveUseCase,
        Depends(lambda: container.resolve(ProductRemoveUseCase)),
    ],
    product_id: Annotated[
        str,
        Path(
            ...,
            description="Product identifier in ULID format",
            examples=["01K4EH5T4YQERHJ99RM1SWYV99"],
        ),
    ],
) -> None:
    use_case.remove_product(product_id)
