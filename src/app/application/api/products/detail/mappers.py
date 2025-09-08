from app.application.api.products.detail.schemas import ProductDetailResponse
from app.domain.models.product import Product


class ProductDetailResponseMapper:

    @staticmethod
    def map(product: Product) -> ProductDetailResponse:
        return ProductDetailResponse(**product.model_dump())
