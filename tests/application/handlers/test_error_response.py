from app.application.handlers.error_response import ErrorResponse


def test_when_values_are_given_and_they_are_valid_then_values_are_retrieved() -> None:
    current = ErrorResponse(
        type="::type::",
        loc=["::loc::"],
        msg="::msg::",
    )

    assert current.type == "::type::"
    assert current.msg == "::msg::"
    assert current.loc == ["::loc::"]


def test_when_optional_values_are_given_and_they_are_valid_then_they_are_retrieved() -> (
    None
):
    error_input = "{'transaction_id': 'f006130d-b029-4b99-ae3b-e0e2f1e07fc9'}"
    url_input = "::url::"

    current = ErrorResponse(
        type="::type::",
        loc=["::loc::"],
        msg="::msg::",
        input=error_input,
        url="::url::",
    )

    assert current.input == error_input
    assert current.url == url_input
