from app.domain.enums.code_enum import ErrorCodeEnum
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundError
from app.domain.models.product import Product
from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.product_view_repository import ProductViewRepository


class ProductDetailUseCase:

    def __init__(
        self,
        product_repository: ProductRepository,
        view_repository: ProductViewRepository,
    ) -> None:
        self.product_repository = product_repository
        self.view_repository = view_repository

    def get_product(self, product_id: str, increment_view: bool) -> Product:
        product = self.product_repository.find_by_id(product_id)
        if product is None:
            raise ResourceNotFoundError(
                code=ErrorCodeEnum.BRAND_NOT_FOUND,
                location=["product_id"],
                message=f"No product found with ID: {product_id}.",
            )

        if increment_view:
            self.view_repository.increment_view(product_id)

        return product
