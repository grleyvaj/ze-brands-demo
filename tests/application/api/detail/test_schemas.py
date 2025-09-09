import pytest
from pydantic import ValidationError

from app.application.api.brands.detail.schemas import BrandDetailResponse


@pytest.mark.parametrize(
    ("field", "value", "expect_error", "expected_msg"),
    [
        # --- name ---
        ("name", "MISSING", True, "Field required"),
        ("name", "x" * 129, True, "at most 128 characters"),
        ("name", "Nike", False, None),
        # --- description ---
        ("description", "", True, "at least 1 character"),
        ("description", "x" * 256, True, "at most 255 characters"),
        ("description", "Sportswear", False, None),
        ("description", None, False, None),
        # --- logo_url ---
        ("logo_url", "", True, "at least 1 character"),
        ("logo_url", "x" * 256, True, "at most 255 characters"),
        ("logo_url", "https://example.com/logo.png", False, None),
        ("logo_url", None, False, None),
    ],
)
def test_brand_detail_response_field_validations(
    field: str,
    value: str | None,
    expect_error: bool,
    expected_msg: str | None,
):
    payload = {
        "id": "01K4G2APXKSSFTYR911GYBDVZX",
        "name": "Nike",
        "description": "Sportswear",
        "logo_url": "https://example.com/logo.png",
    }

    if value == "MISSING":
        payload.pop(field)
    else:
        payload[field] = value

    if expect_error:
        with pytest.raises(ValidationError) as exc:
            BrandDetailResponse(**payload)
        error_msgs = [err["msg"] for err in exc.value.errors()]
        assert any(expected_msg in msg for msg in error_msgs)
    else:
        model = BrandDetailResponse(**payload)
        assert getattr(model, field) == value
