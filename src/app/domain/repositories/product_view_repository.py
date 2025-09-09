from abc import ABC, abstractmethod


class ProductViewRepository(ABC):

    @abstractmethod
    def increment_view(self, product_id: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_views_by_product_id(self, product_id: str) -> None:
        raise NotImplementedError
