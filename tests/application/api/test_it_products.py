from decimal import Decimal

import pytest
import ulid
from fastapi.testclient import TestClient


class TestProductsApiIntegration:

    def test_create_product_then_patched_role_is_checked(
        self,
        test_token: str,
        client: TestClient,
    ) -> None:
        expected_success_code = 200

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {test_token}",
        }
        payload = {
            "brand_id": "01K4KNPTYEBNMX5DP8W0BMTS6C",
            "sku": "::sku::",
            "name": "::name::",
            "price": "49.99",
        }

        response = client.post("/products", headers=headers, json=payload)

        assert response.status_code == expected_success_code
        data = response.json()
        assert data["sku"] == "::sku::"
        assert data["name"] == "::name::"
        assert Decimal(data["price"]) == Decimal("49.99")
        assert data["brand_id"] == "01K4KNPTYEBNMX5DP8W0BMTS6C"

    def test_when_create_product_but_sku_already_exist_then_bad_request_is_retrieved(
        self,
        test_token: str,
        client: TestClient,
    ) -> None:
        expected_bad_request = 400

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {test_token}",
        }
        payload = {
            "brand_id": "01K4KNPTYEBNMX5DP8W0BMTS6C",
            "sku": "SKU-NIKE-001",
            "name": "Test Product",
            "price": "10.0",
        }

        response = client.post("/products", headers=headers, json=payload)

        assert response.status_code == expected_bad_request
        data = response.json()
        first_err = data["detail"][0]
        assert first_err.get("type") == "ALREADY_EXIST_PRODUCT_SKU"
        assert first_err.get("msg") == "Product with SKU 'SKU-NIKE-001' already exists"

    @pytest.mark.parametrize(
        ("field", "value", "expect_error", "expected_msg"),
        [
            ("sku", "SKU1", False, None),
            ("sku", "", True, "at least 1 character"),
            ("sku", "a" * 65, True, "at most 64 characters"),
            ("name", "Valid Product", False, None),
            ("name", "", True, "at least 1 character"),
            ("name", "a" * 256, True, "at most 255 characters"),
            ("price", "0", False, None),
            ("price", "-1", True, "greater than or equal to 0"),
        ],
    )
    def test_when_product_is_create_then_fields_are_validated(
        self,
        field: str,
        value: str | None,
        expect_error: bool,
        expected_msg: str | None,
        client: TestClient,
        test_token: str,
    ) -> None:
        unprocess_status_code = 422
        success_status_code = 200

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {test_token}",
        }
        ulid_str = ulid.new().str
        payload = {
            "brand_id": "01K4KNPTYEBNMX5DP8W0BMTS6C",
            "sku": f"SKU-NIKE-{ulid_str}",
            "name": f"Test Product {ulid_str}",
            "price": "10.0",
        }

        payload[field] = value

        response = client.post("/products", headers=headers, json=payload)

        if not expect_error:
            assert response.status_code == success_status_code
        else:
            assert response.status_code == unprocess_status_code
            body = response.json()
            error_msgs = [err["msg"] for err in body["detail"]]
            assert any(expected_msg in msg for msg in error_msgs)

    def test_when_get_product_detail_successfully(
        self,
        test_token: str,
        client: TestClient,
    ) -> None:
        success_status_code = 200
        expected_price = "129.99"
        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.get("/products/01K4KNQGXMW5KK788YBHJ2D28V", headers=headers)

        assert response.status_code == success_status_code
        data = response.json()
        assert data["id"] == "01K4KNQGXMW5KK788YBHJ2D28V"
        assert data["sku"] == "SKU-NIKE-001"
        assert data["name"] == "Nike Air Max"
        assert data["price"] == expected_price

    def test_when_get_product_detail_but_it_is_not_found(
        self,
        test_token: str,
        client: TestClient,
    ) -> None:
        not_found_status_code = 404
        headers = {"Authorization": f"Bearer {test_token}"}

        non_existent_product_id = "01ZZZZZZZZZZZZZZZZZZZZZZZZ"
        response = client.get(f"/products/{non_existent_product_id}", headers=headers)

        assert response.status_code == not_found_status_code
        body = response.json()
        assert body["detail"] == "No product found with ID: 01ZZZZZZZZZZZZZZZZZZZZZZZZ."

    def test_when_update_successfully_product(
        self,
        test_token: str,
        client: TestClient,
    ) -> None:
        expected_success_code = 200
        expected_price = "99.99"
        headers = {"Authorization": f"Bearer {test_token}"}
        payload = {
            "sku": "UPDATED-SKU",
            "name": "Updated Product",
            "price": "99.99",
            "brand_id": "01K4KNQ7FG9YCRZ3HPF7HRSPWG",
        }
        response = client.put(
            "/products/01K4KNQSQACSWVRGN2NFAWGMT6",
            headers=headers,
            json=payload,
        )

        assert response.status_code == expected_success_code
        data = response.json()
        assert data["sku"] == "UPDATED-SKU"
        assert data["name"] == "Updated Product"
        assert data["price"] == expected_price
        assert data["brand_id"] == "01K4KNQ7FG9YCRZ3HPF7HRSPWG"

    def test_when_update_product_but_product_not_found_then_error_is_thrown(
        self,
        test_token: str,
        client: TestClient,
    ) -> None:
        expected_not_found = 404

        headers = {"Authorization": f"Bearer {test_token}"}
        ulid_str = ulid.new().str
        payload = {
            "brand_id": "01K4KNPTYEBNMX5DP8W0BMTS6C",
            "sku": f"SKU-NIKE-{ulid_str}",
            "name": f"Test Product {ulid_str}",
            "price": "10.0",
        }
        non_existent_product_id = "01ZZZZZZZZZZZZZZZZZZZZZZZZ"
        response = client.put(
            f"/products/{non_existent_product_id}",
            headers=headers,
            json=payload,
        )

        assert response.status_code == expected_not_found

    def test_when_update_product_but_budget_not_found_then_error_is_thrown(
        self,
        test_token: str,
        client: TestClient,
    ) -> None:
        expected_bad_request = 400

        headers = {"Authorization": f"Bearer {test_token}"}
        ulid_str = ulid.new().str
        non_existent_budget_id = "01ZZZZZZZZZZZZZZZZZZZZZZZZ"
        payload = {
            "brand_id": non_existent_budget_id,
            "sku": f"SKU-NIKE-{ulid_str}",
            "name": f"Test Product {ulid_str}",
            "price": "10.0",
        }

        response = client.put(
            "/products/01K4KNQSQACSWVRGN2NFAWGMT6",
            headers=headers,
            json=payload,
        )

        assert response.status_code == expected_bad_request
        data = response.json()
        first_err = data["detail"][0]
        assert first_err.get("type") == "BRAND_NOT_FOUND"
        assert (
            first_err.get("msg")
            == "Brand with ID '01ZZZZZZZZZZZZZZZZZZZZZZZZ' not found"
        )

    def test_when_update_product_but_product_sku_already_exist_then_error_is_thrown(
        self,
        test_token: str,
        client: TestClient,
    ) -> None:
        expected_bad_request = 400

        headers = {"Authorization": f"Bearer {test_token}"}
        ulid_str = ulid.new().str
        payload = {
            "brand_id": "01K4KNPTYEBNMX5DP8W0BMTS6C",
            "sku": "SKU-NIKE-001",
            "name": f"Test Product {ulid_str}",
            "price": "10.0",
        }
        response = client.put(
            "/products/01K4KNQSQACSWVRGN2NFAWGMT6",
            headers=headers,
            json=payload,
        )

        assert response.status_code == expected_bad_request
        data = response.json()
        first_err = data["detail"][0]
        assert first_err.get("type") == "ALREADY_EXIST_PRODUCT_SKU"
        assert first_err.get("msg") == "Product with SKU 'SKU-NIKE-001' already exists"

    def test_views_report(
        self,
        test_token: str,
        client: TestClient,
    ) -> None:
        expected_product_1_view = 10
        expected_product_2_view = 5
        expected_product_3_view = 0
        expected_status_code = 200
        expected_product_size = 6

        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.get("/products/views", headers=headers)

        assert response.status_code == expected_status_code
        data = response.json()

        assert "products" in data
        products = data["products"]
        assert isinstance(products, list)

        assert (
            len(products) == expected_product_size
        ), f"Expected 4 products but got {len(products)}"

        for product in products:
            if product["id"] == "01K4KNQGXMW5KK788YBHJ2D28V":
                assert product["views"] == expected_product_1_view
            elif product["id"] == "01K4KNQSQACSWVRGN2NFAWGMT6":
                assert product["views"] == expected_product_2_view
            else:
                assert product["views"] == expected_product_3_view

    def test_delete_product(
        self,
        test_token: str,
        client: TestClient,
    ) -> None:
        expected_not_content = 204

        headers = {"Authorization": f"Bearer {test_token}"}
        response = client.delete(
            "/products/01K4KNQSQACSWVRGN2NFAWGMT6",
            headers=headers,
        )

        assert response.status_code == expected_not_content
