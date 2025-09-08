from app.application.api.brands.detail.schemas import BrandDetailResponse
from app.domain.models.brand import Brand


class BrandDetailResponseMapper:

    @staticmethod
    def map(brand: Brand) -> BrandDetailResponse:
        return BrandDetailResponse(**brand.model_dump())
