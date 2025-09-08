from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.application.api.brands.create.mappers import BrandCreateInputMapper
from app.application.api.brands.create.schemas import BrandCreateRequest
from app.application.api.brands.detail.mappers import BrandDetailResponseMapper
from app.application.api.brands.detail.schemas import BrandDetailResponse
from app.application.containers import container
from app.core.role_checker import RoleChecker
from app.domain.use_cases.brands.create.brand_create_use_case import BrandCreateUseCase

router = APIRouter(
    prefix="/brands",
    tags=["Brands"],
)


@router.post(
    "",
    dependencies=[Depends(RoleChecker(["ADMIN"]))],
    summary="Create a new brand",
    description="Creates a new brand in the catalog. "
    "Validates that the NAME is unique.",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["name"],
                                "msg": "Brand with NAME 'Nike' already exists",
                                "type": "ALREADY_EXIST_BRAND_NAME",
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
def create_brand(
    request: BrandCreateRequest,
    use_case: Annotated[
        BrandCreateUseCase,
        Depends(lambda: container.resolve(BrandCreateUseCase)),
    ],
) -> BrandDetailResponse:
    brand = use_case.create_brand(
        brand_create_input=BrandCreateInputMapper.map(request),
    )

    return BrandDetailResponseMapper.map(brand)
