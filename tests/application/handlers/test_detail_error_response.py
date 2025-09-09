from app.application.handlers.detail_error_response import DetailErrorResponse
from app.application.handlers.error_response import ErrorResponse


def test_when_values_are_given_and_they_are_valid_then_values_are_retrieved() -> None:
    error = ErrorResponse(
        type="::type::",
        loc=["::loc::"],
        msg="::msg::",
    )
    current = DetailErrorResponse(
        detail=[error],
    )
    detail = current.detail[0]
    assert detail.type == "::type::"
    assert detail.msg == "::msg::"
    assert detail.loc == ["::loc::"]
    assert detail.input is None
    assert detail.url is None


def test_when_optional_values_are_given_and_they_are_valid_then_they_are_retrieved() -> (
    None
):
    error_input = "{'transaction_id': 'f006130d-b029-4b99-ae3b-e0e2f1e07fc9'}"
    url_input = "::url::"

    error = ErrorResponse(
        type="::type::",
        loc=["::loc::"],
        msg="::msg::",
        input=error_input,
        url="::url::",
    )

    current = DetailErrorResponse(
        detail=[error],
    )

    detail = current.detail[0]
    assert detail.input == error_input
    assert detail.url == url_input
