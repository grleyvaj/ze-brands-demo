import pytest
import ulid

from app.domain.enums.code_enum import ErrorCodeEnum
from app.domain.exceptions.data_validation_exception import DataValidationError
from app.domain.use_cases.brands.create.brand_create_input import BrandCreateInput
from app.domain.use_cases.brands.create.brand_create_use_case import BrandCreateUseCase


class TestBrandCreateUseCase:

    def test_create_brand_successfully(self, container_test: dict) -> None:
        use_case: BrandCreateUseCase = container_test[BrandCreateUseCase]

        ulid_str = ulid.new().str
        input_data = BrandCreateInput(
            name=f"Nike{ulid_str}",
            description="Sportswear and athletic footwear",
            logo_url="https://example.com/logos/nike.png",
        )

        brand = use_case.create_brand(input_data)

        assert brand.id is not None
        assert brand.name == f"Nike{ulid_str}"
        assert brand.description == "Sportswear and athletic footwear"
        assert brand.logo_url == "https://example.com/logos/nike.png"

    def test_create_brand_name_already_exists_raises_error(
        self,
        container_test: dict,
    ) -> None:
        use_case: BrandCreateUseCase = container_test[BrandCreateUseCase]

        input_data = BrandCreateInput(
            name="Nike",
            description="Sportswear and athletic footwear",
            logo_url="https://example.com/logos/nike.png",
        )

        with pytest.raises(DataValidationError) as exc_info:
            use_case.create_brand(input_data)
        err = exc_info.value
        assert err.code == ErrorCodeEnum.ALREADY_EXIST_BRAND_NAME
        assert "already exists" in err.message

    @pytest.mark.parametrize(
        ("name", "description", "logo_url", "expect_error", "expected_code"),
        [
            ("Rebook", "", None, False, None),
            ("Puma", None, None, False, None),
        ],
    )
    def test_brand_create_input_validation(
        self,
        container_test: dict,
        name: str,
        description: str | None,
        logo_url: str | None,
        expect_error: bool,
        expected_code: ErrorCodeEnum | None,
    ) -> None:
        use_case: BrandCreateUseCase = container_test[BrandCreateUseCase]

        input_data = BrandCreateInput(
            name=name,
            description=description,
            logo_url=logo_url,
        )

        if expect_error:
            with pytest.raises(DataValidationError) as exc_info:
                use_case.create_brand(input_data)
            assert exc_info.value.code == expected_code
        else:
            brand = use_case.create_brand(input_data)
            assert brand.name == name
            assert brand.description == description
            assert brand.logo_url == logo_url
