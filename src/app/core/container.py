from typing import Any, Callable


class DependencyNotRegisteredError(Exception):
    """Raised when trying to resolve a dependency
    that hasn't been registered in the container."""


class Container:
    def __init__(self):
        self._registry: dict[Any, Callable[[Container], Any]] = {}

    def register(self, key: Any, builder: Callable[["Container"], Any]) -> None:
        self._registry[key] = builder

    def resolve(self, key: Any) -> Any:
        builder = self._registry.get(key)
        if not builder:
            msg = f"No dependency registered for key {key}"
            raise DependencyNotRegisteredError(msg)
        return builder(self)

    def __getitem__(self, key: Any):
        return self.resolve(key)

    def __setitem__(self, key: Any, builder: Callable[["Container"], Any]):
        self.register(key, builder)
