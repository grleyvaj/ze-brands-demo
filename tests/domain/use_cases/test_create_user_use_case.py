import pytest

from app.domain.enums.code_enum import ErrorCodeEnum
from app.domain.exceptions.data_validation_exception import DataValidationError
from app.domain.use_cases.users.create.user_create_input import UserCreateInput
from app.domain.use_cases.users.create.user_create_use_case import UserCreateUseCase


class TestUserCreateUseCase:

    def test_create_successfully_user(
        self,
        container_test: dict,
    ) -> None:
        input_data = UserCreateInput(
            username="::username::",
            email="email@gmail.com",
            password="::password::",
        )

        use_case: UserCreateUseCase = container_test[UserCreateUseCase]
        user = use_case.create_user(input_data)

        assert user.id is not None
        assert user.username == "::username::"
        assert user.email == "email@gmail.com"
        assert user.hashed_password is not None
        assert user.hashed_password != "::password::"

    class TestUserCreateUseCaseAdditional:

        @pytest.mark.parametrize(
            ("username", "email", "password", "expected_error_msg"),
            [
                (
                    "admin",
                    "unique_email@gmail.com",
                    "SuperSecure123!",
                    "already exists",
                ),
                ("unique_user", "email@gmail.com", "SuperSecure123!", "already exists"),
            ],
        )
        def test_user_create_duplicate_username_or_email(
            self,
            container_test: dict,
            username: str,
            email: str,
            password: str,
            expected_error_msg: str,
        ) -> None:
            use_case: UserCreateUseCase = container_test[UserCreateUseCase]

            initial_user = UserCreateInput(
                username="admin",
                email="email@gmail.com",
                password="SuperSecure123!",
            )
            try:
                use_case.create_user(initial_user)
            except DataValidationError:
                pass  # Ignoramos si ya existía, nos interesa el segundo test

            input_data = UserCreateInput(
                username=username,
                email=email,
                password=password,
            )

            with pytest.raises(DataValidationError) as exc_info:
                use_case.create_user(input_data)

            err = exc_info.value
            assert err.code == ErrorCodeEnum.ALREADY_EXIST_USER
            assert expected_error_msg in err.message

        def test_create_user_password_is_hashed(
            self,
            container_test: dict,
        ):
            use_case: UserCreateUseCase = container_test[UserCreateUseCase]

            input_data = UserCreateInput(
                username="testuser",
                email="testuser@gmail.com",
                password="PlainPassword123",
            )
            user = use_case.create_user(input_data)

            assert user.hashed_password != input_data.password
            assert user.hashed_password is not None
