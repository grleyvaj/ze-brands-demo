from decimal import Decimal

import pytest
import ulid

from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundError
from app.domain.repositories.product_repository import ProductRepository
from app.domain.use_cases.products.create.product_create_input import ProductCreateInput
from app.domain.use_cases.products.edit.product_update_input import ProductUpdateInput
from app.infrastructure.persistence.postgres_product_repository import (
    PostgresProductRepository,
)


class TestPostgresProductRepository:

    def test_create_product_persists_in_db(self, container_test: dict) -> None:
        repo: PostgresProductRepository = container_test[ProductRepository]

        ulid_str = ulid.new().str
        input_data = ProductCreateInput(
            sku=f"SKU-{ulid_str}",
            name=f"Test Product {ulid_str}",
            price=Decimal("99.99"),
            brand_id="01K4KNPTYEBNMX5DP8W0BMTS6C",  # Nike
        )

        product = repo.create(input_data)

        assert product.id is not None
        assert product.sku == f"SKU-{ulid_str}"
        assert product.name == f"Test Product {ulid_str}"
        assert product.price == Decimal("99.99")
        assert product.brand_id == "01K4KNPTYEBNMX5DP8W0BMTS6C"
        assert repo.exists_by_sku(product.sku) is True

    def test_find_by_id_and_sku(self, container_test: dict) -> None:
        repo: PostgresProductRepository = container_test[ProductRepository]

        ulid_str = ulid.new().str
        input_data = ProductCreateInput(
            sku=f"SKU-{ulid_str}",
            name=f"Find Product {ulid_str}",
            price=Decimal("10.50"),
            brand_id="01K4KNQ7FG9YCRZ3HPF7HRSPWG",  # Adidas
        )
        created = repo.create(input_data)

        found_by_id = repo.find_by_id(created.id)
        assert found_by_id is not None
        assert found_by_id.id == created.id

        found_by_sku = repo.find_by_sku(created.sku)
        assert found_by_sku is not None
        assert found_by_sku.sku == created.sku

    def test_update_product(self, container_test: dict) -> None:
        repo: PostgresProductRepository = container_test[ProductRepository]

        ulid_str = ulid.new().str
        product = repo.create(
            ProductCreateInput(
                sku=f"SKU-{ulid_str}",
                name=f"Old Name {ulid_str}",
                price=Decimal("50.00"),
                brand_id="01K4KNPTYEBNMX5DP8W0BMTS6C",
            ),
        )

        update_input = ProductUpdateInput(
            sku="FAKE-SKU",
            name=f"New Name {ulid_str}",
            price=Decimal("75.00"),
            brand_id="01K4KNPTYEBNMX5DP8W0BMTS6C",
        )

        updated = repo.update(product.id, update_input)

        assert updated.id == product.id
        assert updated.name == f"New Name {ulid_str}"
        assert updated.price == Decimal("75.00")

    def test_update_nonexistent_product_raises(self, container_test: dict) -> None:
        repo: PostgresProductRepository = container_test[ProductRepository]

        with pytest.raises(ResourceNotFoundError):
            repo.update(
                product_id="nonexistent-id",
                product_update=ProductUpdateInput(
                    sku="FAKE-SKU",
                    name="Should Fail",
                    price=Decimal("99.99"),
                    brand_id="01K4KNPTYEBNMX5DP8W0BMTS6C",
                ),
            )

    def test_delete_product(self, container_test: dict) -> None:
        repo: PostgresProductRepository = container_test[ProductRepository]

        ulid_str = ulid.new().str
        product = repo.create(
            ProductCreateInput(
                sku=f"SKU-{ulid_str}",
                name=f"Delete Product {ulid_str}",
                price=Decimal("20.00"),
                brand_id="01K4KNPTYEBNMX5DP8W0BMTS6C",
            ),
        )

        repo.delete_by_id(product.id)

        assert repo.find_by_id(product.id) is None

    def test_list_products_returns_views(self, container_test: dict) -> None:
        repo: PostgresProductRepository = container_test[ProductRepository]

        ulid_str = ulid.new().str
        repo.create(
            ProductCreateInput(
                sku=f"SKU-{ulid_str}",
                name=f"List Product {ulid_str}",
                price=Decimal("15.00"),
                brand_id="01K4KNQ7FG9YCRZ3HPF7HRSPWG",
            ),
        )

        products = repo.list_products()
        assert any("List Product" in prod.name for prod in products)

        products_for_adidas = repo.list_products("01K4KNQ7FG9YCRZ3HPF7HRSPWG")
        assert all(prod.id is not None for prod in products_for_adidas)
