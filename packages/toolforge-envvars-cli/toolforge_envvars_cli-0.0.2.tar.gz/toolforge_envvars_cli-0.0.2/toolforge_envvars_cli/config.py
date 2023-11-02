from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any

from toolforge_weld.config import Config, Section, load_config


@dataclass
class EnvvarsConfig(Section):
    _NAME_: str = field(default="envvars", init=False)
    endpoint: str = "/envvars/v1"

    @classmethod
    def from_dict(cls, my_dict: dict[str, Any]):
        params = {}
        if "endpoint" in my_dict:
            params["endpoint"] = my_dict["endpoint"]
        return cls(**params)


@lru_cache(maxsize=None)
def get_loaded_config() -> Config:
    return load_config(client_name="envvars", extra_sections=[EnvvarsConfig])
