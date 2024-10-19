from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager
from typing import Literal, NamedTuple, Optional, TYPE_CHECKING


from fastapi import FastAPI
from typing_extensions import Self

if TYPE_CHECKING:
    from utils.config import VoiceConfig

class VoiceApp(FastAPI):
    def __init__(
        self,
        *,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        config: VoiceConfig,
    ):
        self.loop: asyncio.AbstractEventLoop = (
            loop or asyncio.get_event_loop_policy().get_event_loop()
        )
        super().__init__(
            title="Voice App",
            version="x",
            description="",
            loop=self.loop,
            redoc_url="/docs",
            docs_url=None,
            lifespan=self.lifespan,
        )
        self.config = config

    @asynccontextmanager
    async def lifespan(self, app: Self):
        yield
