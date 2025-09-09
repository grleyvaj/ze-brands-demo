from decimal import Decimal
from unittest.mock import MagicMock

import pytest
import ulid

from app.domain.exceptions.data_validation_exception import DataValidationError
from app.domain.models.product import Product
from app.domain.services.product_update_event import ProductUpdateEvent
from app.domain.use_cases.products.edit.product_update_input import ProductUpdateInput
from app.domain.use_cases.products.edit.product_update_use_case import (
    ProductUpdateUseCase,
)


@pytest.fixture
def mock_product_repository() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_brand_repository() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_notification_service() -> MagicMock:
    return MagicMock()


@pytest.fixture
def use_case(
    mock_product_repository: MagicMock,
    mock_brand_repository: MagicMock,
    mock_notification_service: MagicMock,
) -> ProductUpdateUseCase:
    return ProductUpdateUseCase(
        product_repository=mock_product_repository,
        brand_repository=mock_brand_repository,
        notification_service=mock_notification_service,
    )


ulid_str = ulid.new().str


def make_product(
    product_id: str = "p1",
    sku: str = f"SKU1{ulid_str}",
    name: str = f"Product 1{ulid_str}",
    price: Decimal = Decimal("10.0"),
    brand_id: str = "01K4KNQ7FG9YCRZ3HPF7HRSPWG",
) -> Product:
    return Product(
        id=product_id,
        sku=sku,
        name=name,
        price=price,
        brand_id=brand_id,
    )


def make_update_input(
    sku: str = f"SKU1{ulid_str}",
    name: str = f"Product 1{ulid_str}",
    price: Decimal = Decimal("10.0"),
    brand_id: str = "01K4KNQ7FG9YCRZ3HPF7HRSPWG",
) -> ProductUpdateInput:
    return ProductUpdateInput(
        sku=sku,
        name=name,
        price=price,
        brand_id=brand_id,
    )


def test_update_product_brand_not_found(
    use_case: ProductUpdateUseCase,
    mock_brand_repository: MagicMock,
) -> None:
    product_id = "p1"
    update_input = make_update_input()

    mock_brand_repository.exists_by_id.return_value = False

    with pytest.raises(DataValidationError) as exc:
        use_case.update_product(product_id, update_input)

    assert "not found" in str(exc.value)


def test_update_product_success(
    use_case: ProductUpdateUseCase,
    mock_product_repository: MagicMock,
    mock_brand_repository: MagicMock,
    mock_notification_service: MagicMock,
) -> None:
    product_id = "p1"
    update_input = make_update_input()

    mock_brand_repository.exists_by_id.return_value = True
    mock_product_repository.find_by_sku.return_value = None

    existing = make_product(
        product_id=product_id,
        sku=update_input.sku,
        name=update_input.name,
        price=update_input.price,
        brand_id=update_input.brand_id,
    )
    mock_product_repository.find_by_id.return_value = existing
    mock_product_repository.update.return_value = existing

    result = use_case.update_product(product_id, update_input)

    assert isinstance(result, Product)
    mock_product_repository.update.assert_called_once_with(
        product_id=product_id,
        product_update=update_input,
    )
    mock_notification_service.notify.assert_not_called()


def test_notify_changes_no_changes(
    use_case: ProductUpdateUseCase,
    mock_product_repository: MagicMock,
    mock_brand_repository: MagicMock,
    mock_notification_service: MagicMock,
) -> None:
    product_id = "p1"
    existing = make_product(product_id=product_id)
    update_input = make_update_input(
        sku=existing.sku,
        name=existing.name,
        price=existing.price,
        brand_id=existing.brand_id,
    )

    mock_brand_repository.exists_by_id.return_value = True
    mock_product_repository.find_by_sku.return_value = existing
    mock_product_repository.find_by_id.return_value = existing
    mock_product_repository.update.return_value = existing

    use_case.update_product(product_id, update_input)

    mock_notification_service.notify.assert_not_called()


def test_notify_changes_with_changes(
    use_case: ProductUpdateUseCase,
    mock_product_repository: MagicMock,
    mock_notification_service: MagicMock,
) -> None:
    product_id = "p1"
    existing = make_product(name="Old Name")
    update_input = make_update_input(name="New Name")

    mock_product_repository.find_by_id.return_value = existing

    use_case._notify_changes(product_id, update_input)

    mock_notification_service.notify.assert_called_once()
    args, kwargs = mock_notification_service.notify.call_args
    event: ProductUpdateEvent = kwargs["event"]
    assert "name" in event.changes
    assert event.changes["name"]["old"] == "Old Name"
    assert event.changes["name"]["new"] == "New Name"
