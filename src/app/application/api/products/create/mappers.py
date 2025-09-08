from app.application.api.products.create.schemas import ProductCreateRequest
from app.domain.use_cases.products.create.product_create_input import ProductCreateInput


class ProductCreateInputMapper:

    @staticmethod
    def map(request: ProductCreateRequest) -> ProductCreateInput:
        return ProductCreateInput(**request.model_dump())
