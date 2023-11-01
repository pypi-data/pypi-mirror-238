import httpx

from .. import ty
from ..models import EnvAwaiting, EnvCreating, EnvReturning
from .base import BaseClient


class Envs2(BaseClient):
    def create(self, body: EnvCreating) -> EnvReturning:
        res = self.request(
            "POST",
            endpoint="create",
            data=body,
            return_model=EnvReturning,
            timeout=httpx.Timeout(5.0, read=30.0),
        )
        return ty.cast(EnvReturning, res)

    async def create_async(self, body: EnvCreating) -> EnvReturning:
        res = self.request_async(
            "POST",
            endpoint="create",
            data=body,
            return_model=EnvReturning,
            timeout=httpx.Timeout(5.0, read=30.0),
        )
        return ty.cast(EnvReturning, res)

    def await_env(self, body: EnvAwaiting) -> EnvReturning:
        res = self.request(
            "POST",
            endpoint="await",
            data=body,
            return_model=EnvReturning,
            timeout=httpx.Timeout(5.0, read=30.0),
        )
        return ty.cast(EnvReturning, res)

    async def await_env_async(self, body: EnvAwaiting) -> EnvReturning:
        res = self.request_async(
            "POST",
            endpoint="await",
            data=body,
            return_model=EnvReturning,
            timeout=httpx.Timeout(5.0, read=30.0),
        )
        return ty.cast(EnvReturning, res)
