import pytest

from app.core.container import Container, DependencyNotRegisteredError


def test_register_and_resolve():
    container = Container()

    container.register("service", lambda _: "my_service")
    result = container.resolve("service")

    assert result == "my_service"


def test_resolve_not_registered_raises():
    container = Container()

    with pytest.raises(DependencyNotRegisteredError) as exc_info:
        container.resolve("unknown")

    assert "No dependency registered for key unknown" in str(exc_info.value)


def test_getitem_and_setitem_syntax():
    container = Container()

    container["service"] = lambda _: "my_service"
    result = container["service"]

    assert result == "my_service"


def test_builder_receives_container():
    container = Container()

    def builder(c: Container) -> str:
        assert isinstance(c, Container)
        return "service_with_container"

    container.register("service", builder)
    result = container.resolve("service")

    assert result == "service_with_container"
