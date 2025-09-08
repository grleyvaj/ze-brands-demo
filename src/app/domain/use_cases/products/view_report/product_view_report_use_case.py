from app.domain.models.product import ProductView
from app.domain.repositories.product_repository import ProductRepository


class ProductViewReportUseCase:

    def __init__(
        self,
        product_repository: ProductRepository,
    ) -> None:
        self.product_repository = product_repository

    def view_report(self, brand_id: str | None) -> list[ProductView]:
        return self.product_repository.list_products(brand_id=brand_id)
