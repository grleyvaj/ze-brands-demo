from app.domain.helpers.datetime_generator import get_now_datetime
from app.domain.helpers.ulid_generator import generate_ulid
from app.domain.models.brand import Brand
from app.domain.use_cases.brands.create.brand_create_input import BrandCreateInput
from app.infrastructure.entity.brand_entity import BrandEntity


class BrandMapper:

    @staticmethod
    def map_to_entity(brand: BrandCreateInput) -> BrandEntity:
        date_now = get_now_datetime()

        return BrandEntity(
            id=generate_ulid(),
            name=brand.name,
            description=brand.description,
            logo_url=brand.logo_url,
            created_at=date_now,
            updated_at=date_now,
        )

    @staticmethod
    def map_to_model(brand: BrandEntity) -> Brand:
        return Brand(
            id=brand.id,
            name=brand.name,
            description=brand.description,
            logo_url=brand.logo_url,
        )
