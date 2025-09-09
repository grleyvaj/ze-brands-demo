import os
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from jose import jwt

USERNAME_TEST = "newaccessuser"
PASSWORD_TEST = "SuperSecure123!"


class TestAccessApiIntegration:

    def test_sigup_user_successfully(
        self,
        client: TestClient,
    ) -> None:
        expected_ok_code = 200
        payload = {
            "username": USERNAME_TEST,
            "email": "newaccessuser@example.com",
            "password": PASSWORD_TEST,
        }

        response = client.post("/sigup", json=payload)

        assert response.status_code == expected_ok_code
        data = response.json()
        assert data["username"] == USERNAME_TEST
        assert data["email"] == "newaccessuser@example.com"
        assert data["role"] == "ANONYMOUS"
        assert "id" in data

    def test_sigup_existing_user_then_fails(
        self,
        client: TestClient,
    ) -> None:
        expected_bad_request = 400
        payload = {
            "username": "admin",
            "email": "admin@example.com",
            "password": PASSWORD_TEST,
        }

        response = client.post("/sigup", json=payload)

        assert response.status_code == expected_bad_request
        body = response.json()
        first_err = body["detail"][0]
        assert first_err.get("type") == "ALREADY_EXIST_USER"

    @pytest.mark.parametrize(
        ("field", "value", "expect_error", "expected_msg"),
        [
            ("username", "us", True, "at least 3 characters"),
            ("username", "a" * 51, True, "at most 50 characters"),
            ("email", "a@b", True, "valid email address"),
            (
                "email",
                "x" * 101 + "@example.com",
                True,
                "Value should have at most 100 items",
            ),
            ("password", "short", True, "at least 8 characters"),
        ],
    )
    def test_sigup_field_validation(
        self,
        field: str,
        value: str | None,
        expect_error: bool,
        expected_msg: str | None,
        client: TestClient,
    ) -> None:
        success_status_code = 200
        unprocess_status_code = 422

        payload = {
            "username": "validusername",
            "email": "validuser@example.com",
            "password": PASSWORD_TEST,
        }
        payload[field] = value

        response = client.post("/sigup", json=payload)

        if expect_error:
            assert response.status_code == unprocess_status_code
            error_msgs = [err["msg"] for err in response.json()["detail"]]
            assert any(expected_msg in msg for msg in error_msgs)
        else:
            assert response.status_code == success_status_code

    def test_login_user_successfully(
        self,
        client: TestClient,
    ) -> None:
        expected_ok_code = 200
        payload = {
            "username": USERNAME_TEST,
            "password": PASSWORD_TEST,
        }

        response = client.post("/login", json=payload)

        assert response.status_code == expected_ok_code
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

        decoded = jwt.decode(
            data["access_token"],
            os.environ.get("SECRET_KEY", "supersecretkey12345"),
            algorithms=[os.environ.get("ALGORITHM", "HS256")],
        )
        assert decoded["sub"]

    def test_login_invalid_credentials(
        self,
        client: TestClient,
    ) -> None:
        unauthorized_code = 401
        payload = {
            "username": USERNAME_TEST,
            "password": "wrongpassword",
        }

        response = client.post("/login", json=payload)

        assert response.status_code == unauthorized_code
        body = response.json()
        assert body["detail"] in ["Invalid credentials", "Unauthorized"]

    def test_login_expired_token_is_rejected(self, client: TestClient):
        error_status_code = 405

        expired_payload = {
            "sub": "01K4H2DVXW24B09C20NZWMB50T",
            "role": "ANONYMOUS",
            "exp": datetime.now(UTC) - timedelta(minutes=1),
        }
        expired__token = jwt.encode(
            expired_payload,
            os.environ.get("SECRET_KEY", "supersecretkey12345"),
            algorithm=os.environ.get("ALGORITHM", "HS256"),
        )
        headers = {"Authorization": f"Bearer {expired__token}"}

        response = client.get("/products", headers=headers)

        assert response.status_code == error_status_code
