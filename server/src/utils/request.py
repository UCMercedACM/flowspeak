from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi import Request

if TYPE_CHECKING:
    from core import VoiceApp


class RouteRequest(Request):
    app: VoiceApp
