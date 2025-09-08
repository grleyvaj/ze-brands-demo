from abc import ABC, abstractmethod

from app.domain.models.product import Product, ProductView
from app.domain.use_cases.products.create.product_create_input import ProductCreateInput
from app.domain.use_cases.products.edit.product_update_input import ProductUpdateInput


class ProductRepository(ABC):

    @abstractmethod
    def create(
        self,
        product_create: ProductCreateInput,
    ) -> Product:
        raise NotImplementedError

    @abstractmethod
    def exists_by_sku(self, sku: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, product_id: str) -> Product | None:
        raise NotImplementedError

    @abstractmethod
    def find_by_sku(self, sku: str) -> Product | None:
        raise NotImplementedError

    @abstractmethod
    def update(self, product_id: str, product_update: ProductUpdateInput) -> Product:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, user_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_products(self, brand_id: str) -> list[ProductView]:
        raise NotImplementedError
