from app.domain.enums.code_enum import ErrorCodeEnum
from app.domain.exceptions.data_validation_exception import DataValidationError
from app.domain.models.product import Product
from app.domain.repositories.brand_repository import BrandRepository
from app.domain.repositories.product_repository import ProductRepository
from app.domain.use_cases.products.create.product_create_input import ProductCreateInput


class ProductCreateUseCase:

    def __init__(
        self,
        product_repository: ProductRepository,
        brand_repository: BrandRepository,
    ) -> None:
        self.product_repository = product_repository
        self.brand_repository = brand_repository

    def create_product(self, create_input: ProductCreateInput) -> Product:
        self._apply_business_validation(create_input)
        return self.product_repository.create(product_create=create_input)

    def _apply_business_validation(
        self,
        product_create_input: ProductCreateInput,
    ) -> None:
        if not self.brand_repository.exists_by_id(product_create_input.brand_id):
            raise DataValidationError(
                code=ErrorCodeEnum.BRAND_NOT_FOUND,
                location=["brand_id"],
                message=f"Brand with ID '{product_create_input.brand_id}' not found",
            )
        if self.product_repository.exists_by_sku(product_create_input.sku):
            raise DataValidationError(
                code=ErrorCodeEnum.ALREADY_EXIST_PRODUCT_SKU,
                location=["sku"],
                message=f"Product with SKU '{product_create_input.sku}' already exists",
            )
