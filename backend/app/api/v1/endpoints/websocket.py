"""
WebSocket API端点
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.websocket_service import WebSocketService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket连接端点"""
    await WebSocketService.handle_websocket(websocket, client_id)


@router.websocket("/ws")
async def websocket_endpoint_no_id(websocket: WebSocket):
    """WebSocket连接端点（无客户端ID）"""
    await WebSocketService.handle_websocket(websocket) 