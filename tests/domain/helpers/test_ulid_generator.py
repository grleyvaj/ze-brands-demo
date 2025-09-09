import ulid

from app.domain.helpers.ulid_generator import generate_ulid


def test_generate_ulid_returns_string_and_length():
    expected_ulid_size = 26

    result = generate_ulid()

    assert isinstance(result, str)
    assert len(result) == expected_ulid_size


def test_generate_ulid_is_valid_ulid():
    result = generate_ulid()
    parsed = ulid.parse(result)
    assert str(parsed) == result
