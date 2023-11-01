from typing import Any
from pydantic._internal._model_construction import ModelMetaclass  # noqa
from pydantic._internal._generics import PydanticGenericMetadata  # noqa


class SpaceModelMetaclass(ModelMetaclass):
    def __new__(
        cls,
        cls_name: str,
        bases: tuple[type[Any], ...],
        namespace: dict[str, Any],
        __pydantic_generic_metadata__: PydanticGenericMetadata | None = None,
        __pydantic_reset_parent_namespace__: bool = True,
        **kwargs: Any,
    ):
        class_obj = super(SpaceModelMetaclass, cls).__new__(
            cls,
            cls_name,
            bases,
            namespace,
            __pydantic_generic_metadata__,
            __pydantic_reset_parent_namespace__,
            **kwargs,
        )

        return class_obj
