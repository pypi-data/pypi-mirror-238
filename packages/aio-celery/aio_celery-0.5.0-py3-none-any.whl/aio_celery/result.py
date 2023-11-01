import asyncio
import json
import time
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from .app import Celery
from .exceptions import TimeoutError


class AsyncResult:
    def __init__(
        self,
        id: str,  # noqa: A002
        *,
        app: "Celery",
    ) -> None:
        self.id = id
        self.task_id = id
        self._cache = None
        self.result_backend = app.result_backend

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: {self.task_id}>"

    async def _get_task_meta(self) -> Dict[str, Any]:
        if self.result_backend is None:
            raise RuntimeError("Result backend has not been enabled")
        if self._cache is None:
            value = await self.result_backend.get(f"celery-task-meta-{self.task_id}")
            if value is None:
                return {"result": None, "status": "PENDING"}
            self._cache = json.loads(value)
        return self._cache

    @property
    async def result(self) -> Any:
        return (await self._get_task_meta())["result"]

    @property
    async def state(self) -> str:
        return str((await self._get_task_meta())["status"])

    async def get(self, timeout: Optional[float] = None, interval: float = 0.5) -> Any:
        """Wait until task is ready, and return its result."""

        value = await self._get_task_meta()
        start = time.monotonic()
        while value == {"result": None, "status": "PENDING"}:
            await asyncio.sleep(interval)
            if timeout is not None and (time.monotonic() - start) > timeout:
                raise TimeoutError("The operation timed out.")
            value = await self._get_task_meta()
        return value["result"]
