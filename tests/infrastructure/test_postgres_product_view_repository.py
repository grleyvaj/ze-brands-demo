from decimal import Decimal

import ulid

from app.domain.repositories.product_repository import ProductRepository
from app.domain.repositories.product_view_repository import ProductViewRepository
from app.domain.use_cases.products.create.product_create_input import ProductCreateInput
from app.infrastructure.persistence.postgres_product_view_repository import (
    PostgresProductViewRepository,
)


class TestPostgresProductViewRepository:

    def test_increment_view_creates_new_entry(self, container_test: dict) -> None:
        expected_count_before_view = 0
        expected_count_after_view = 1

        repo: PostgresProductViewRepository = container_test[ProductViewRepository]
        product_repo: ProductRepository = container_test[ProductRepository]

        ulid_str = ulid.new().str
        product = product_repo.create(
            ProductCreateInput(
                sku=f"SKU-{ulid_str}",
                name=f"TestProduct{ulid_str}",
                price=Decimal("100.0"),
                brand_id="01K4KNPTYEBNMX5DP8W0BMTS6C",
            ),
        )

        views = product_repo.list_products(product.brand_id)
        product_view = next(v for v in views if v.id == product.id)
        assert product_view.view == expected_count_before_view

        repo.increment_view(product.id)

        views = product_repo.list_products(product.brand_id)
        product_view = next(v for v in views if v.id == product.id)
        assert product_view.view == expected_count_after_view

    def test_increment_view_increments_existing_entry(
        self,
        container_test: dict,
    ) -> None:
        expected_count_view = 2

        repo: PostgresProductViewRepository = container_test[ProductViewRepository]
        product_repo: ProductRepository = container_test[ProductRepository]

        ulid_str = ulid.new().str
        product = product_repo.create(
            ProductCreateInput(
                sku=f"SKU-{ulid_str}",
                name=f"TestProduct{ulid_str}",
                price=Decimal("50.0"),
                brand_id="01K4KNPTYEBNMX5DP8W0BMTS6C",
            ),
        )

        repo.increment_view(product.id)
        repo.increment_view(product.id)

        views = product_repo.list_products(product.brand_id)
        product_view = next(v for v in views if v.id == product.id)
        assert product_view.view == expected_count_view

    def test_delete_views_by_product_id(self, container_test: dict) -> None:
        expected_prod_1_count_view = 2
        expected_prod_2_count_view = 0

        repo: PostgresProductViewRepository = container_test[ProductViewRepository]
        product_repo: ProductRepository = container_test[ProductRepository]

        ulid_str = ulid.new().str
        product = product_repo.create(
            ProductCreateInput(
                sku=f"SKU-{ulid_str}",
                name=f"TestProduct{ulid_str}",
                price=Decimal("25.0"),
                brand_id="01K4KNPTYEBNMX5DP8W0BMTS6C",
            ),
        )

        repo.increment_view(product.id)
        repo.increment_view(product.id)

        views = product_repo.list_products(product.brand_id)
        product_view = next(v for v in views if v.id == product.id)
        assert product_view.view == expected_prod_1_count_view

        repo.delete_views_by_product_id(product.id)

        views = product_repo.list_products(product.brand_id)
        product_view = next(v for v in views if v.id == product.id)
        assert product_view.view == expected_prod_2_count_view
