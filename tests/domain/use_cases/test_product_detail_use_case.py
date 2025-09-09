from unittest.mock import MagicMock

import pytest

from app.domain.enums.code_enum import ErrorCodeEnum
from app.domain.exceptions.resource_not_found_exception import ResourceNotFoundError
from app.domain.models.product import Product
from app.domain.use_cases.products.detail.product_detail_use_case import (
    ProductDetailUseCase,
)


@pytest.fixture
def mock_product_repository():
    return MagicMock()


@pytest.fixture
def mock_view_repository():
    return MagicMock()


@pytest.fixture
def use_case(
    mock_product_repository: MagicMock,
    mock_view_repository: MagicMock,
):
    return ProductDetailUseCase(
        product_repository=mock_product_repository,
        view_repository=mock_view_repository,
    )


def test_get_product_returns_product_without_increment(
    use_case: ProductDetailUseCase,
    mock_product_repository: MagicMock,
    mock_view_repository: MagicMock,
) -> None:
    product = Product(
        id="01K4KNQGXMW5KK788YBHJ2D28V",
        sku="SKU-123",
        name="Test Product",
        price=100.0,
        brand_id="01K4KNPTYEBNMX5DP8W0BMTS6C",
    )
    mock_product_repository.find_by_id.return_value = product

    result = use_case.get_product(product_id=product.id, increment_view=False)

    assert result == product
    mock_product_repository.find_by_id.assert_called_once_with(product.id)
    mock_view_repository.increment_view.assert_not_called()


def test_get_product_returns_product_and_increments_view(
    use_case: ProductDetailUseCase,
    mock_product_repository: MagicMock,
    mock_view_repository: MagicMock,
) -> None:
    product = Product(
        id="01K4KNQGXMW5KK788YBHJ2D28V",
        sku="SKU-456",
        name="Another Product",
        price=200.0,
        brand_id="01K4KNPTYEBNMX5DP8W0BMTS6C",
    )
    mock_product_repository.find_by_id.return_value = product

    result = use_case.get_product(product_id=product.id, increment_view=True)

    assert result == product
    mock_product_repository.find_by_id.assert_called_once_with(product.id)
    mock_view_repository.increment_view.assert_called_once_with(product.id)


def test_get_product_raises_not_found_error(
    use_case: ProductDetailUseCase,
    mock_product_repository: MagicMock,
) -> None:
    mock_product_repository.find_by_id.return_value = None
    product_id = "non-existing-id"

    with pytest.raises(ResourceNotFoundError) as exc_info:
        use_case.get_product(product_id=product_id, increment_view=True)

    err = exc_info.value
    assert err.code == ErrorCodeEnum.BRAND_NOT_FOUND
    assert err.location == ["product_id"]
    assert str(err) == f"No product found with ID: {product_id}."
