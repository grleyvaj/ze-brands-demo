from decimal import Decimal

import pytest
import ulid

from app.domain.enums.code_enum import ErrorCodeEnum
from app.domain.exceptions.data_validation_exception import DataValidationError
from app.domain.use_cases.products.create.product_create_input import ProductCreateInput
from app.domain.use_cases.products.create.product_create_use_case import (
    ProductCreateUseCase,
)


class TestProductCreateUseCase:

    def test_create_product_successfully(self, container_test: dict) -> None:
        use_case: ProductCreateUseCase = container_test[ProductCreateUseCase]

        ulid_str = ulid.new().str
        input_data = ProductCreateInput(
            sku=f"SKU{ulid_str}",
            name=f"Nombre{ulid_str}",
            price=Decimal("99.9"),
            brand_id="01K4KNQ7FG9YCRZ3HPF7HRSPWG",
        )

        product = use_case.create_product(input_data)

        assert product.id is not None
        assert product.sku == f"SKU{ulid_str}"
        assert product.name == f"Nombre{ulid_str}"
        assert product.price == Decimal("99.9")
        assert product.brand_id == "01K4KNQ7FG9YCRZ3HPF7HRSPWG"

    def test_create_sku_product_already_exists_raises_error(
        self,
        container_test: dict,
    ) -> None:
        use_case: ProductCreateUseCase = container_test[ProductCreateUseCase]

        ulid_str = ulid.new().str
        input_data = ProductCreateInput(
            sku="SKU-NIKE-001",
            name=f"Nombre{ulid_str}",
            price=Decimal("99.9"),
            brand_id="01K4KNQ7FG9YCRZ3HPF7HRSPWG",
        )

        with pytest.raises(DataValidationError) as exc_info:
            use_case.create_product(input_data)

        err = exc_info.value
        assert err.code == ErrorCodeEnum.ALREADY_EXIST_PRODUCT_SKU
        assert "already exists" in err.message

    def test_create_product_bud_brand_not_found_raises_error(
        self,
        container_test: dict,
    ) -> None:
        use_case: ProductCreateUseCase = container_test[ProductCreateUseCase]

        ulid_str = ulid.new().str
        input_data = ProductCreateInput(
            sku="SKU-NIKE-001",
            name=f"Nombre{ulid_str}",
            price=Decimal("99.9"),
            brand_id="ANY",
        )

        with pytest.raises(DataValidationError) as exc_info:
            use_case.create_product(input_data)

        err = exc_info.value
        assert err.code == ErrorCodeEnum.BRAND_NOT_FOUND
        assert "not found" in err.message
