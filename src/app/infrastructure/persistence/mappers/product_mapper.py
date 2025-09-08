from app.domain.helpers.datetime_generator import get_now_datetime
from app.domain.helpers.ulid_generator import generate_ulid
from app.domain.models.product import Product
from app.domain.use_cases.products.create.product_create_input import ProductCreateInput
from app.infrastructure.entity.product_entity import ProductEntity


class ProductMapper:

    @staticmethod
    def map_to_entity(product: ProductCreateInput) -> ProductEntity:
        date_now = get_now_datetime()

        return ProductEntity(
            id=generate_ulid(),
            sku=product.sku,
            name=product.name,
            price=product.price,
            brand_id=product.brand_id,
            created_at=date_now,
            updated_at=date_now,
        )

    @staticmethod
    def map_to_model(entity: ProductEntity) -> Product:
        return Product(
            id=entity.id,
            sku=entity.sku,
            name=entity.name,
            price=entity.price,
            brand_id=entity.brand_id,
        )
