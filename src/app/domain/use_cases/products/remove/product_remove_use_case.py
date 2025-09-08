from app.domain.repositories.product_repository import ProductRepository


class ProductRemoveUseCase:

    def __init__(
        self,
        product_repository: ProductRepository,
    ) -> None:
        self.product_repository = product_repository

    def remove_product(self, product_id: str) -> None:
        self.product_repository.delete_by_id(product_id)
