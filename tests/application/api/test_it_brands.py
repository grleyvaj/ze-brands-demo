import pytest
from fastapi.testclient import TestClient


class TestBrandsApiIntegration:

    def test_create_brand_then_patched_role_is_checked(
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
            "name": "::name::",
            "description": "::description::",
            "logo_url": "::logo_url::",
        }

        response = client.post("/brands", headers=headers, json=payload)

        assert response.status_code == expected_success_code

        data = response.json()
        assert data["name"] == "::name::"
        assert data["description"] == "::description::"
        assert data["logo_url"] == "::logo_url::"

    def test_when_create_brand_but_name_already_exist_then_bad_request_is_retrieved(
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
            "name": "Nike",
            "description": "::description::",
            "logo_url": "::logo_url::",
        }

        response = client.post("/brands", headers=headers, json=payload)

        assert response.status_code == expected_bad_request
        data = response.json()
        first_err = data["detail"][0]
        assert first_err.get("type") == "ALREADY_EXIST_BRAND_NAME"
        assert first_err.get("msg") == "Brand with NAME 'Nike' already exists"

    @pytest.mark.parametrize(
        ("field", "value", "expect_error", "expected_msg"),
        [
            ("name", "a", False, None),
            ("name", "a" * 128, False, None),
            ("name", None, True, "Field required"),
            ("name", "", True, "at least 1 character"),
            ("name", "a" * 129, True, "at most 128 characters"),
        ],
    )
    def test_when_brand_create_then_name_is_validated(
        self,
        field: str,
        value: str | None,
        expect_error: bool,
        expected_msg: str | None,
        client: TestClient,
        test_token: str,
    ) -> None:
        success_status_code = 200
        unprocess_status_code = 422

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {test_token}",
        }

        payload = {
            "name": "Valid Brand 1",
            "description": "A valid description",
            "logo_url": "https://example.com/logo.png",
        }

        if value is None:
            payload.pop(field, None)
        else:
            payload[field] = value

        response = client.post("/brands", headers=headers, json=payload)

        if not expect_error:
            assert response.status_code == success_status_code
        else:
            assert response.status_code == unprocess_status_code
            body = response.json()
            error_msgs = [err["msg"] for err in body["detail"]]
            assert any(expected_msg in msg for msg in error_msgs)

    @pytest.mark.parametrize(
        ("field", "value", "expect_error", "expected_msg"),
        [
            ("description", "ok", False, None),
            ("description", "", True, "at least 1 character"),
            ("description", "a" * 256, True, "at most 255 characters"),
        ],
    )
    def test_when_brand_create_then_description_is_validated(
        self,
        field: str,
        value: str | None,
        expect_error: bool,
        expected_msg: str | None,
        client: TestClient,
        test_token: str,
    ) -> None:
        success_status_code = 200
        unprocess_status_code = 422

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {test_token}",
        }

        payload = {
            "name": "Valid Brand 2",
            "description": "A valid description",
            "logo_url": "https://example.com/logo.png",
        }
        if value is None:
            payload.pop(field, None)
        else:
            payload[field] = value

        response = client.post("/brands", headers=headers, json=payload)

        if not expect_error:
            assert response.status_code == success_status_code
        else:
            assert response.status_code == unprocess_status_code
            body = response.json()
            error_msgs = [err["msg"] for err in body["detail"]]
            assert any(expected_msg in msg for msg in error_msgs)

    @pytest.mark.parametrize(
        ("field", "value", "expect_error", "expected_msg"),
        [
            ("logo_url", None, False, None),
            ("logo_url", "", True, "at least 1 character"),
            ("logo_url", "u" * 256, True, "at most 255 characters"),
        ],
    )
    def test_when_brand_create_then_logo_url_is_validated(
        self,
        field: str,
        value: str | None,
        expect_error: bool,
        expected_msg: str | None,
        client: TestClient,
        test_token: str,
    ) -> None:
        success_status_code = 200
        unprocess_status_code = 422

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {test_token}",
        }

        payload = {
            "name": "Valid Brand 3",
            "description": "A valid description",
            "logo_url": "https://example.com/logo.png",
        }
        if value is None:
            payload.pop(field, None)
        else:
            payload[field] = value

        response = client.post("/brands", headers=headers, json=payload)

        if not expect_error:
            assert response.status_code == success_status_code
        else:
            assert response.status_code == unprocess_status_code
            body = response.json()
            error_msgs = [err["msg"] for err in body["detail"]]
            assert any(expected_msg in msg for msg in error_msgs)
