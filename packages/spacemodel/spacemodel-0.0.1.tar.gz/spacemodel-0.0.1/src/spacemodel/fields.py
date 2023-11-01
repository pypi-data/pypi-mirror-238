from typing import Annotated
from pydantic import (
    AfterValidator,
    PlainSerializer,
    WithJsonSchema,
)

import datetime


_string_serializer_args = (
    AfterValidator(lambda x: x),
    PlainSerializer(lambda x: str(x), return_type=str, when_used='unless-none'),
    WithJsonSchema({'type': 'string'}, mode='serialization'),
)


LargeInt = Annotated[int, *_string_serializer_args]
LargeFloat = Annotated[float, *_string_serializer_args]

UtcTimestamp = Annotated[
    datetime.datetime,
    AfterValidator(lambda x: x),
    PlainSerializer(lambda x: str(x.timestamp()), return_type=str, when_used='unless-none'),
    WithJsonSchema({'type': 'integer'}, mode='serialization'),
]
