from unittest.mock import MagicMock

import pytest

from app.domain.use_cases.products.remove.product_remove_use_case import (
    ProductRemoveUseCase,
)


@pytest.fixture
def mock_product_repository() -> MagicMock:
    return MagicMock()


@pytest.fixture
def mock_view_repository() -> MagicMock:
    return MagicMock()


@pytest.fixture
def use_case(
    mock_product_repository: MagicMock,
    mock_view_repository: MagicMock,
) -> ProductRemoveUseCase:
    return ProductRemoveUseCase(
        product_repository=mock_product_repository,
        view_repository=mock_view_repository,
    )


def test_remove_product_calls_repositories_in_order(
    use_case: ProductRemoveUseCase,
    mock_product_repository: MagicMock,
    mock_view_repository: MagicMock,
) -> None:
    product_id = "p123"

    use_case.remove_product(product_id)

    mock_view_repository.delete_views_by_product_id.assert_called_once_with(product_id)
    mock_product_repository.delete_by_id.assert_called_once_with(product_id)

    calls = [
        ("delete_views_by_product_id", (product_id,), {}),
        ("delete_by_id", (product_id,), {}),
    ]

    actual_calls = [
        (call[0], call[1], call[2])
        for call in (
            mock_view_repository.method_calls + mock_product_repository.method_calls
        )
    ]

    assert actual_calls == calls


def test_remove_product_no_exceptions_if_not_found(
    use_case: ProductRemoveUseCase,
    mock_product_repository: MagicMock,
    mock_view_repository: MagicMock,
) -> None:
    product_id = "p404"

    mock_view_repository.delete_views_by_product_id.return_value = None
    mock_product_repository.delete_by_id.return_value = None

    use_case.remove_product(product_id)

    mock_view_repository.delete_views_by_product_id.assert_called_once_with(product_id)
    mock_product_repository.delete_by_id.assert_called_once_with(product_id)
