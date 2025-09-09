import os
from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from jose import jwt

USERNAME_TEST = "newadmin"
PASSWORD_TEST = "SuperSecure123!"


class TestUsersApiIntegration:

    def test_create_user_successfully(
        self,
        test_token: str,
        client: TestClient,
    ) -> None:
        expected_ok_code = 200
        headers = {"Authorization": f"Bearer {test_token}"}
        payload = {
            "username": USERNAME_TEST,
            "email": "newadmin@example.com",
            "password": PASSWORD_TEST,
        }

        response = client.post("/users", headers=headers, json=payload)

        assert response.status_code == expected_ok_code
        data = response.json()
        assert data["username"] == "newadmin"
        assert data["email"] == "newadmin@example.com"
        assert data["role"] == "ADMIN"
        assert "hashed_password" in data

    def test_non_admin_user_create_new_user_then_unauthorized_is_retrieved(
        self,
        client: TestClient,
    ) -> None:
        expected_unauthorized = 401

        payload = {
            "sub": "01K4H2DVXW24B09C20NZWMB50T",
            "role": "ANONYMOUS",
            "exp": datetime.now(UTC) + timedelta(minutes=60),
        }
        anon_token = jwt.encode(
            payload,
            os.environ.get("SECRET_KEY", "supersecretkey12345"),
            algorithm=os.environ.get("ALGORITHM", "HS256"),
        )
        headers = {"Authorization": f"Bearer {anon_token}"}

        response = client.post("/users", headers=headers, json=payload)

        assert response.status_code == expected_unauthorized

    def test_create_user_with_existing_username_fails(
        self,
        test_token: str,
        client: TestClient,
    ) -> None:
        expected_bad_request = 400

        headers = {"Authorization": f"Bearer {test_token}"}
        payload = {
            "username": "admin",
            "email": "another@example.com",
            "password": "AnotherPass123",
        }
        response = client.post("/users", headers=headers, json=payload)

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
                "Value should have at most 100 items after validation, not 113",
            ),
            ("password", "short", True, "at least 8 characters"),
        ],
    )
    def test_user_create_field_validation(
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

        headers = {"Authorization": f"Bearer {test_token}"}
        payload = {
            "username": "username123",
            "email": "emial123@example.com",
            "password": "SuperSecure123!",
        }
        payload[field] = value

        response = client.post("/users", headers=headers, json=payload)

        if expect_error:
            assert response.status_code == unprocess_status_code
            error_msgs = [err["msg"] for err in response.json()["detail"]]
            assert any(expected_msg in msg for msg in error_msgs)
        else:
            assert response.status_code == success_status_code

    def test_update_user_email_successfully(
        self,
        test_token: str,
        client: TestClient,
    ) -> None:
        expected_ok_code = 200

        headers = {"Authorization": f"Bearer {test_token}"}
        payload = {"email": "updatedadmin@example.com"}
        user_id = "01K4KNRC1B66FPMG6YSCBMJDK4"

        response = client.put(f"/users/{user_id}", headers=headers, json=payload)
        assert response.status_code == expected_ok_code

        data = response.json()
        assert data["email"] == "updatedadmin@example.com"
        assert data["username"] == "admin"

    def test_update_user_not_found(self, test_token: str, client: TestClient):
        expected_not_found = 404

        headers = {"Authorization": f"Bearer {test_token}"}
        payload = {"email": "nonexistent@example.com"}
        non_existent_id = "01ZZZZZZZZZZZZZZZZZZZZZZZZ"

        response = client.put(
            f"/users/{non_existent_id}",
            headers=headers,
            json=payload,
        )

        assert response.status_code == expected_not_found

    def test_non_admin_user_update_an_user_then_unauthorized_is_retrieved(
        self,
        client: TestClient,
    ) -> None:
        expected_unauthorized = 401

        payload = {
            "sub": "01K4H2DVXW24B09C20NZWMB50T",
            "role": "ANONYMOUS",
            "exp": datetime.now(UTC) + timedelta(minutes=60),
        }
        anon_token = jwt.encode(
            payload,
            os.environ.get("SECRET_KEY", "supersecretkey12345"),
            algorithm=os.environ.get("ALGORITHM", "HS256"),
        )
        headers = {"Authorization": f"Bearer {anon_token}"}
        user_id = "01K4KNRC1B66FPMG6YSCBMJDK4"
        response = client.put(f"/users/{user_id}", headers=headers, json=payload)

        assert response.status_code == expected_unauthorized

    def test_delete_user_successfully(
        self,
        test_token: str,
        client: TestClient,
    ) -> None:
        expected_not_content = 204

        headers = {"Authorization": f"Bearer {test_token}"}
        user_id = "01K4KNRJKABX0FS4Q3RJEQ5RX5"  # anon

        response = client.delete(f"/users/{user_id}", headers=headers)

        assert response.status_code == expected_not_content

    def test_non_admin_user_remove_an_user_then_unauthorized_is_retrieved(
        self,
        client: TestClient,
    ) -> None:
        expected_unauthorized = 401

        payload = {
            "sub": "01K4H2DVXW24B09C20NZWMB50T",
            "role": "ANONYMOUS",
            "exp": datetime.now(UTC) + timedelta(minutes=60),
        }
        anon_token = jwt.encode(
            payload,
            os.environ.get("SECRET_KEY", "supersecretkey12345"),
            algorithm=os.environ.get("ALGORITHM", "HS256"),
        )

        headers = {"Authorization": f"Bearer {anon_token}"}
        user_id = "01K4KNRC1B66FPMG6YSCBMJDK4"

        response = client.delete(f"/users/{user_id}", headers=headers)

        assert response.status_code == expected_unauthorized

    def test_login_user_successfully(self, client: TestClient):
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

    def test_login_user_invalid_credentials(self, client: TestClient):
        unauthorized_code = 401

        payload = {
            "username": USERNAME_TEST,
            "password": "wrongpassword",
        }

        response = client.post("/login", json=payload)

        assert response.status_code == unauthorized_code
        body = response.json()
        assert body["detail"] == "Invalid credentials"
