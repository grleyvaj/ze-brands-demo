from app.domain.enums.code_enum import ErrorCodeEnum
from app.domain.exceptions.data_validation_exception import DataValidationError
from app.domain.models.brand import Brand
from app.domain.repositories.brand_repository import BrandRepository
from app.domain.use_cases.brands.create.brand_create_input import BrandCreateInput


class BrandCreateUseCase:

    def __init__(
        self,
        brand_repository: BrandRepository,
    ) -> None:
        self.brand_repository = brand_repository

    def create_brand(self, brand_create_input: BrandCreateInput) -> Brand:
        self._apply_business_validation_create(brand_create_input)
        return self.brand_repository.create(brand=brand_create_input)

    def _apply_business_validation_create(self, create_input: BrandCreateInput) -> None:
        if self.brand_repository.exists_by_name(create_input.name):
            raise DataValidationError(
                code=ErrorCodeEnum.ALREADY_EXIST_BRAND_NAME,
                location=["name"],
                message=f"Brand with NAME '{create_input.name}' already exists",
            )
