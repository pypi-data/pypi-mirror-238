from __future__ import annotations

import json
from functools import wraps
from pathlib import Path
from typing import Any

import requests
from toolforge_weld.api_client import ToolforgeClient
from toolforge_weld.config import Config
from toolforge_weld.kubernetes_config import Kubeconfig

ERROR_STRINGS = {
    "SERVICE_DOWN_ERROR": (
        "The envvars service seems to be down – please retry in a few minutes.\nIf the problem persists, "
        + "please contact us or open a bug:\nsee https://phabricator.wikimedia.org/T324822"
    ),
    "UNKNOWN_ERROR": (
        "An unknown error occured while trying to perform this operation.\nIf the problem persists, "
        + "please contact us or open a bug:\nsee https://phabricator.wikimedia.org/T324822"
    ),
}

USER_AGENT = "envvars client"


class EnvvarsClientError(Exception):
    def to_str(self) -> str:
        err_str = str(self)
        try:
            err_dict = json.loads(err_str)
            return err_dict["message"]
        except json.decoder.JSONDecodeError:
            return err_str


class InvalidEnvvarName(EnvvarsClientError):
    pass


class BadRequest(EnvvarsClientError):
    pass


class Unauthorized(EnvvarsClientError):
    pass


class NotFound(EnvvarsClientError):
    pass


def with_api_error(func):
    @wraps(func)
    def _inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.ConnectionError as error:
            raise EnvvarsClientError(ERROR_STRINGS["SERVICE_DOWN_ERROR"]) from error

        except requests.HTTPError as error:
            if error.response.status_code == 400:
                raise BadRequest(error.response.text) from error

            if error.response.status_code == 401:
                raise Unauthorized(error.response.text) from error

            if error.response.status_code == 404:
                raise NotFound(str(error)) from error

            if error.response.status_code == 422:
                raise InvalidEnvvarName(error.response.text) from error

            raise EnvvarsClientError(ERROR_STRINGS["UNKNOWN_ERROR"] + f"\nOriginal error: {error}") from error

    return _inner


class EnvvarsClient(ToolforgeClient):
    def __init__(
        self,
        kubeconfig: Kubeconfig,
        server: str,
        endpoint_prefix: str,
        user_agent: str,
    ):
        super().__init__(
            kubeconfig=kubeconfig,
            server=server + endpoint_prefix,
            user_agent=user_agent,
        )

    @classmethod
    def from_config(cls, config: Config, kubeconfig: Path):
        return cls(
            endpoint_prefix=config.envvars.endpoint,
            kubeconfig=Kubeconfig.load(kubeconfig.expanduser().resolve()),
            server=config.api_gateway.url,
            user_agent=USER_AGENT,
        )

    @with_api_error
    def get(self, url: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        return super().get(url=url, json=json)

    @with_api_error
    def post(self, url: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        return super().post(url=url, json=json)

    @with_api_error
    def put(self, url: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        return super().put(url=url, json=json)

    @with_api_error
    def delete(self, url: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        return super().delete(url=url, json=json)
