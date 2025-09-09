from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.product_view_repository import ProductViewRepository


class ProductRemoveUseCase:

    def __init__(
        self,
        product_repository: ProductRepository,
        view_repository: ProductViewRepository,
    ) -> None:
        self.product_repository = product_repository
        self.view_repository = view_repository

    def remove_product(self, product_id: str) -> None:
        self.view_repository.delete_views_by_product_id(product_id)
        self.product_repository.delete_by_id(product_id)
