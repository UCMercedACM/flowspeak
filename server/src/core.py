from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, Optional

import google.generativeai as genai
from fastapi import FastAPI
from typing_extensions import Self

import db

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
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.chat = self.model.start_chat(
            history=[
                {"role": "user", "parts": "Hello"},
                {"role": "model", "parts": "Answer the prompt"},
            ]
        )

    @asynccontextmanager
    async def lifespan(self, app: Self):
        await db.init_db()

        # Configure this last so *hopefully* event loop doesn't block?
        genai.configure(api_key=self.config["app"]["api_key"])
        yield
