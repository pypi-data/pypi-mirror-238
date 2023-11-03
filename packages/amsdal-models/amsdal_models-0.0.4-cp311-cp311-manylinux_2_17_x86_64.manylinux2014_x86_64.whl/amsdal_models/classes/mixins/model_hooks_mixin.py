from typing import Any


class ModelHooksMixin:
    def pre_init(self, *, is_new_object: bool, kwargs: dict[str, Any]) -> None:
        pass

    def post_init(self, *, is_new_object: bool, kwargs: dict[str, Any]) -> None:
        pass

    def pre_create(self) -> None:
        pass

    def post_create(self) -> None:
        pass

    def pre_update(self) -> None:
        pass

    def post_update(self) -> None:
        pass

    def pre_delete(self) -> None:
        pass

    def post_delete(self) -> None:
        pass
