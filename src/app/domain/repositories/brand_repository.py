from abc import ABC, abstractmethod

from app.domain.models.brand import Brand
from app.domain.use_cases.brands.create.brand_create_input import BrandCreateInput


class BrandRepository(ABC):

    @abstractmethod
    def create(
        self,
        brand: BrandCreateInput,
    ) -> Brand:
        raise NotImplementedError

    @abstractmethod
    def exists_by_id(self, brand_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        raise NotImplementedError
