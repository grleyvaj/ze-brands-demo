from app.application.api.brands.detail.mappers import BrandDetailResponseMapper
from app.application.api.brands.detail.schemas import BrandDetailResponse
from app.domain.models.brand import Brand


class TestBrandDetailResponseMapper:

    def test_map_should_return_brand_detail_response(self) -> None:
        brand = Brand(
            id="01K4G2APXKSSFTYR911GYBDVZX",
            name="Nike",
            description="Sportswear and athletic footwear",
            logo_url="https://example.com/logos/nike.png",
        )

        result = BrandDetailResponseMapper.map(brand)

        assert isinstance(result, BrandDetailResponse)
        assert result.id == brand.id
        assert result.name == brand.name
        assert result.description == brand.description
        assert result.logo_url == brand.logo_url

    def test_map_with_optional_fields_none(self) -> None:
        brand = Brand(
            id="01K4G2APXKSSFTYR911GYBDVZX",
            name="Adidas",
            description=None,
            logo_url=None,
        )

        result = BrandDetailResponseMapper.map(brand)

        assert isinstance(result, BrandDetailResponse)
        assert result.id == brand.id
        assert result.name == brand.name
        assert result.description is None
        assert result.logo_url is None
