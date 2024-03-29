from pathlib import Path
from typing import Any, Type, Union, TypeVar
import json

C = TypeVar("C")


def materialize_element(path: Union[str, Path], cls: Type[C]) -> C:
    with open(path, mode="r") as fh:
        json_blob = json.load(fh)
    return cls(**json_blob)
