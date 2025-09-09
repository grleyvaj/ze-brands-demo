from unittest.mock import MagicMock

import pytest

from app.domain.models.product import ProductView
from app.domain.use_cases.products.view_report.product_view_report_use_case import (
    ProductViewReportUseCase,
)


@pytest.fixture
def mock_product_repository() -> MagicMock:
    return MagicMock()


@pytest.fixture
def use_case(mock_product_repository: MagicMock) -> ProductViewReportUseCase:
    return ProductViewReportUseCase(product_repository=mock_product_repository)


def make_product_view(product_id: str = "p1") -> ProductView:
    return ProductView(
        id=product_id,
        name="Test Product",
        view=5,
    )


def test_view_report_with_brand_id(
    use_case: ProductViewReportUseCase,
    mock_product_repository: MagicMock,
) -> None:
    brand_id = "b1"
    expected = [make_product_view("p1")]
    mock_product_repository.list_products.return_value = expected

    result = use_case.view_report(brand_id)

    assert result == expected
    mock_product_repository.list_products.assert_called_once_with(brand_id=brand_id)


def test_view_report_without_brand_id(
    use_case: ProductViewReportUseCase,
    mock_product_repository: MagicMock,
) -> None:
    expected = [make_product_view("p2"), make_product_view("p3")]
    mock_product_repository.list_products.return_value = expected

    result = use_case.view_report(None)

    assert result == expected
    mock_product_repository.list_products.assert_called_once_with(brand_id=None)
