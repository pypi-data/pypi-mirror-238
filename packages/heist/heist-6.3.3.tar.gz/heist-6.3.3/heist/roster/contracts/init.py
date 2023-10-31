from typing import Any
from typing import Dict
from typing import Mapping


def sig_read(hub, roster_file: str = "") -> Dict[str, Any]:
    ...


async def post_read(hub, ctx):
    ret = ctx.ret or {}
    for data in ret.values():
        assert isinstance(data, Mapping)
    return ret
