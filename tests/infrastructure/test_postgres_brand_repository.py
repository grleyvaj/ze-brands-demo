import ulid

from app.domain.repositories.brand_repository import BrandRepository
from app.domain.use_cases.brands.create.brand_create_input import BrandCreateInput
from app.infrastructure.persistence.postgres_brand_repository import (
    PostgresBrandRepository,
)


class TestPostgresBrandRepository:

    def test_create_brand_persists_in_db(self, container_test: dict) -> None:
        repo: PostgresBrandRepository = container_test[BrandRepository]

        ulid_str = ulid.new().str
        input_data = BrandCreateInput(
            name=f"TestBrand{ulid_str}",
            description="Integration test brand",
            logo_url="http://logo.com/test.png",
        )

        brand = repo.create(input_data)

        assert brand.id is not None
        assert brand.name == f"TestBrand{ulid_str}"

        brand_by_id = repo.exists_by_id(brand.id)
        assert brand_by_id is True

        brand_by_name = repo.exists_by_name(f"TestBrand{ulid_str}")
        assert brand_by_name is True

    def test_exists_by_id_and_name(self, container_test: dict) -> None:
        repo: PostgresBrandRepository = container_test[BrandRepository]

        nike_id = "01K4KNPTYEBNMX5DP8W0BMTS6C"

        assert repo.exists_by_id(nike_id) is True
