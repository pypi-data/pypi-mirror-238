from typing import Optional, Union, Generator, List
from pydantic import BaseModel


import os
import datetime

from .meta import SpaceModelMetaclass
from .base import Base, DetaData, DetaQuery, get_base, enumerate_all
from .fields import LargeInt, LargeFloat, UtcTimestamp


class SpaceModel(BaseModel, metaclass=SpaceModelMetaclass):
    __basename__: Optional[str] = None
    __basehost__: Optional[str] = None

    key: Optional[str] = None

    def __init_subclass__(cls, basename: Optional[str] = None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__basename__ = basename or cls.__basename__

    @classmethod
    def basename(cls) -> str:  # noqa
        if hasattr(cls, '__basename__') and cls.__basename__:
            return cls.__basename__
        return cls.__name__.lower()

    @classmethod
    def basehost(cls) -> Optional[str]:  # noqa
        if hasattr(cls, '__basehost__') and cls.__basehost__:
            return cls.__basehost__
        return os.environ.get('DETA_BASE_HOST')

    @classmethod
    def set_project_key(cls, project_key: str):
        cls.__project_key__ = project_key

    @classmethod
    def get_project_key(cls) -> Optional[str]:  # noqa
        return cls.__project_key__ or os.environ.get('DETA_PROJECT_KEY')

    @classmethod
    def base(cls, project_key: Optional[str] = None, *, project_id: Optional[str] = None) -> Base:
        return get_base(
            cls.basename(),
            project_key or cls.get_project_key(),
            project_id=project_id,
            host=cls.basehost(),
        )

    @classmethod
    def _get(cls, key: str) -> Optional[dict]:
        return cls.base().get(key)

    def _save(
        self,
        key: Optional[str] = None,
        *,
        expire_in: Union[int, float, datetime.timedelta, None] = None,
        expire_at: Union[int, float, datetime.datetime, None] = None,
        fail_if_exists: bool = False,
        **kwargs,
    ):
        base_ = self.base()

        # expire_in is only allowed as `int` normally.
        if isinstance(expire_in, datetime.timedelta):
            expire_in = expire_in.total_seconds()

        if isinstance(expire_in, float):
            expire_in = int(expire_in)

        model_data = self.model_dump(**kwargs)

        if fail_if_exists:
            model_data = base_.insert(model_data, key, expire_in=expire_in, expire_at=expire_at)
        else:
            model_data = base_.put(model_data, key, expire_in=expire_in, expire_at=expire_at)

        self.key = model_data.get('key')

    @classmethod
    def get(cls, key: str) -> Optional['SpaceModel']:
        model_data = cls._get(key)
        if model_data is not None:
            return cls.model_validate(model_data)

    @classmethod
    def get_or_fail(cls, key: str) -> 'SpaceModel':
        model_data = cls._get(key)
        if model_data is None:
            raise Exception('No item retrieved')
        return cls.model_validate(model_data)

    @classmethod
    def first(cls, query: Optional[DetaQuery] = None) -> Optional['SpaceModel']:
        model_data = cls.base().fetch(query, limit=1).items

        if len(model_data):
            return cls.model_validate(model_data[0])

    @classmethod
    def first_or_fail(cls, query: Optional[DetaQuery] = None) -> 'SpaceModel':
        model_data = cls.base().fetch(query, limit=1).items

        if not len(model_data):
            raise Exception('No entries')

        return cls.model_validate(model_data[0])

    @classmethod
    def last(cls, query: Optional[DetaQuery] = None) -> Optional['SpaceModel']:
        model_data = cls.base().fetch(query, limit=1, desc=True).items

        if len(model_data):
            return cls.model_validate(model_data[0])

    @classmethod
    def last_or_fail(cls, query: Optional[DetaQuery] = None) -> 'SpaceModel':
        model_data = cls.base().fetch(query, limit=1, desc=True).items

        if not len(model_data):
            raise Exception('No entries')

        return cls.model_validate(model_data[0])

    @classmethod
    def enumerate(
        cls,
        query: Optional[DetaQuery] = None,
        limit: int = 1000,
        desc: bool = False,
    ) -> Generator['SpaceModel', None, None]:
        yield from (cls.model_validate(data) for data in enumerate_all(cls.base(), query, limit, desc))

    @classmethod
    def fetch(
        cls,
        query: Optional[DetaQuery] = None,
        limit: int = 1000,
        desc: bool = False,
    ) -> List['SpaceModel']:
        return list(cls.enumerate(query, limit, desc))

    @classmethod
    def create(
        cls,
        source: Union[DetaData, BaseModel],
        *,
        expire_in: Union[int, float, datetime.timedelta, None] = None,
        expire_at: Union[int, float, datetime.datetime, None] = None,
    ) -> 'SpaceModel':
        from_attributes = isinstance(source, BaseModel)
        item = cls.model_validate(source, from_attributes=from_attributes)
        item._save(item.key, expire_in=expire_in, expire_at=expire_at, fail_if_exists=True)
        return item

    @classmethod
    def count(cls, query: Optional[DetaQuery] = None) -> int:
        return sum(1 for _ in cls.enumerate(query))

    @classmethod
    def truncate(cls, query: Optional[DetaQuery] = None):
        base_ = cls.base()
        for item in cls.enumerate(query):
            base_.delete(item.key)

    @classmethod
    def delete(cls, item: 'SpaceModel'):
        cls.base().delete(item.key)

    @classmethod
    def update(
        cls,
        updates: Optional[dict],
        key: str,
        *,
        expire_in: Union[int, float, datetime.timedelta, None] = None,
        expire_at: Union[int, float, datetime.datetime, None] = None,
    ):
        base_ = cls.base()

        # expire_in is only allowed as `int` normally.
        if isinstance(expire_in, datetime.timedelta):
            expire_in = expire_in.total_seconds()

        if isinstance(expire_in, float):
            expire_in = int(expire_in)

        base_.update(updates, key, expire_in=expire_in, expire_at=expire_at)

    @classmethod
    def update_many(
        cls,
        updates: Optional[dict],
        query: Optional[DetaQuery] = None,
        *,
        expire_in: Union[int, float, datetime.timedelta, None] = None,
        expire_at: Union[int, float, datetime.datetime, None] = None,
    ):
        base_ = cls.base()

        # expire_in is only allowed as `int` normally.
        if isinstance(expire_in, datetime.timedelta):
            expire_in = expire_in.total_seconds()

        if isinstance(expire_in, float):
            expire_in = int(expire_in)

        for item in cls.enumerate(query):
            base_.update(updates, item.key, expire_in=expire_in, expire_at=expire_at)

    def save(
        self,
        *,
        expire_in: Union[int, float, datetime.timedelta, None] = None,
        expire_at: Union[int, float, datetime.datetime, None] = None,
        exclude_none: bool = False,
        exclude_unset: bool = False,
    ):
        self._save(
            self.key,
            expire_in=expire_in,
            expire_at=expire_at,
            exclude_none=exclude_none,
            exclude_unset=exclude_unset,
        )

    def refresh(self):
        if self.key:
            model_data = self._get(self.key)
            model = self.model_validate(model_data)

            for key, value in model:
                if hasattr(self, key):
                    setattr(self, key, value)
