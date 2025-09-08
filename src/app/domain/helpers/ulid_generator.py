import ulid


def generate_ulid() -> str:
    """
    Returns ulid identifier using the current date and time in UTC.
    """
    return str(ulid.new())
