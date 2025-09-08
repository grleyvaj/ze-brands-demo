from app.application.api.brands.create.schemas import BrandCreateRequest
from app.domain.use_cases.brands.create.brand_create_input import BrandCreateInput


class BrandCreateInputMapper:

    @staticmethod
    def map(request: BrandCreateRequest) -> BrandCreateInput:
        return BrandCreateInput(**request.model_dump())
