from typing import Dict, Set

from fastapi import WebSocket

from backend.app.common.models import WSMessage, WSMessagePayloadLog, WSMessagePayloadDownload, WSMessagePayloadProcess

TActiveConnections = Dict[str, Set[WebSocket]]


class WSManager:
    def __init__(self):
        self.active_connections: TActiveConnections = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        self.active_connections.setdefault(user_id, set()).add(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        self.active_connections[user_id].remove(websocket)

    async def send_message(self, user_id: str, message: WSMessage):
        if user_id in self.active_connections:
            for websock in self.active_connections[user_id]:
                await websock.send_text(message.model_dump_json())

    async def send_log(self, user_id: str, log_message: str):
        await self.send_message(user_id,
                                WSMessage(message_payload=WSMessagePayloadLog(message=log_message), message_type="log"))

    async def send_error(self, user_id: str, error_message: str):
        await self.send_message(user_id, WSMessage(message_payload=WSMessagePayloadLog(message=error_message),
                                                   message_type="error"))

    async def send_info(self, user_id: str, error_message: str):
        await self.send_message(user_id, WSMessage(message_payload=WSMessagePayloadLog(message=error_message),
                                                   message_type="info"))

    async def send_link(self, user_id: str, link: str, file_name: str, script_name: str, created_datetime: float):
        await self.send_message(user_id,
                                WSMessage(message_payload=WSMessagePayloadDownload(link=link, file_name=file_name,
                                                                                   script_name=script_name,
                                                                                   created_at=created_datetime),
                                          message_type="link"))

    async def send_process_status(self, user_id: str, is_running: bool, script_name: str = None):
        await self.send_message(user_id,
                                WSMessage(message_payload=WSMessagePayloadProcess(is_running=is_running,
                                                                                  script_name=script_name),
                                          message_type="process"))


ws_manager = WSManager()
