from app.application.api.products.edit.schemas import ProductUpdateRequest
from app.domain.use_cases.products.edit.product_update_input import ProductUpdateInput


class ProductUpdateInputMapper:

    @staticmethod
    def map(request: ProductUpdateRequest) -> ProductUpdateInput:
        return ProductUpdateInput(**request.model_dump())
