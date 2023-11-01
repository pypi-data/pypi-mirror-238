from typing import Optional, Union, List
from deta import Deta, _Base as Base  # noqa


DetaData = Union[dict, list, str, int, bool]
DetaQuery = Union[dict, list]


def get_base(
    name: str,
    project_key: Optional[str] = None,
    *,
    project_id: Optional[str] = None,
    host: Optional[str] = None,
) -> Base:
    deta = Deta(project_key, project_id=project_id)
    base = deta.Base(name, host)
    return base


def enumerate_all(base: Base, query: DetaQuery, limit: int = 1000, desc: bool = False) -> List[DetaData]:
    res = base.fetch(query, limit=limit, desc=desc)
    yield from res.items

    while res.last:
        res = base.fetch(query, limit=limit, desc=desc, last=res.last)
        yield from res.items
