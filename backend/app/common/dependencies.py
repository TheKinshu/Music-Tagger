from fastapi import Request
from backend.app.intergration.websocket import WSManager


def get_ws_manager(request: Request) -> WSManager:
    """Retrieve WSManager instance from app.state."""
    return request.app.state.ws_manager