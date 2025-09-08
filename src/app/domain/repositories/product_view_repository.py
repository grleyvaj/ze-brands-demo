from abc import ABC, abstractmethod


class ProductViewRepository(ABC):

    @abstractmethod
    def increment_view(self, product_id: str) -> None:
        raise NotImplementedError
