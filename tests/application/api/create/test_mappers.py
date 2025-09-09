from app.application.api.brands.create.mappers import BrandCreateInputMapper
from app.application.api.brands.create.schemas import BrandCreateRequest
from app.domain.use_cases.brands.create.brand_create_input import BrandCreateInput


class TestBrandCreateInputMapper:

    def test_map_should_return_brand_create_input(self) -> None:
        request = BrandCreateRequest(
            name="Nike",
            description="Sports brand",
            logo_url="https://addidas.com/logo.png",
        )

        result = BrandCreateInputMapper.map(request)

        assert isinstance(result, BrandCreateInput)
        assert result.name == "Nike"
        assert result.description == "Sports brand"
        assert result.logo_url == "https://addidas.com/logo.png"

    def test_map_with_minimal_fields(self) -> None:
        request = BrandCreateRequest(name="Adidas")
        result = BrandCreateInputMapper.map(request)

        assert isinstance(result, BrandCreateInput)
        assert result.name == "Adidas"
        assert getattr(result, "description", None) is None
        assert getattr(result, "logo_url", None) is None
