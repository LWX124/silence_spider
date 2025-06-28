"""
WebSocket服务
用于实时通信和状态更新
"""
import asyncio
import json
import logging
from typing import Dict, List, Any
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime

logger = logging.getLogger(__name__)


class ConnectionManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.connection_data: Dict[WebSocket, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str = None):
        """建立WebSocket连接"""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.connection_data[websocket] = {
            'client_id': client_id,
            'connected_at': datetime.now(),
            'last_activity': datetime.now()
        }
        logger.info(f"WebSocket连接建立: {client_id}")
    
    def disconnect(self, websocket: WebSocket):
        """断开WebSocket连接"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            client_id = self.connection_data.get(websocket, {}).get('client_id')
            del self.connection_data[websocket]
            logger.info(f"WebSocket连接断开: {client_id}")
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """发送个人消息"""
        try:
            await websocket.send_text(message)
            self.connection_data[websocket]['last_activity'] = datetime.now()
        except Exception as e:
            logger.error(f"发送个人消息失败: {e}")
            self.disconnect(websocket)
    
    async def broadcast(self, message: str):
        """广播消息给所有连接"""
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
                self.connection_data[connection]['last_activity'] = datetime.now()
            except Exception as e:
                logger.error(f"广播消息失败: {e}")
                disconnected.append(connection)
        
        # 清理断开的连接
        for connection in disconnected:
            self.disconnect(connection)
    
    async def send_json(self, data: Dict[str, Any], websocket: WebSocket = None):
        """发送JSON数据"""
        message = json.dumps(data, ensure_ascii=False, default=str)
        if websocket:
            await self.send_personal_message(message, websocket)
        else:
            await self.broadcast(message)


# 全局连接管理器实例
manager = ConnectionManager()


class WebSocketService:
    """WebSocket服务类"""
    
    @staticmethod
    async def handle_websocket(websocket: WebSocket, client_id: str = None):
        """处理WebSocket连接"""
        await manager.connect(websocket, client_id)
        try:
            while True:
                # 接收客户端消息
                data = await websocket.receive_text()
                try:
                    message = json.loads(data)
                    await WebSocketService.process_message(websocket, message)
                except json.JSONDecodeError:
                    logger.warning(f"无效的JSON消息: {data}")
                
        except WebSocketDisconnect:
            manager.disconnect(websocket)
        except Exception as e:
            logger.error(f"WebSocket处理错误: {e}")
            manager.disconnect(websocket)
    
    @staticmethod
    async def process_message(websocket: WebSocket, message: Dict[str, Any]):
        """处理接收到的消息"""
        message_type = message.get('type')
        
        if message_type == 'ping':
            # 心跳检测
            await manager.send_json({'type': 'pong', 'timestamp': datetime.now().isoformat()}, websocket)
        
        elif message_type == 'subscribe':
            # 订阅特定事件
            event = message.get('event')
            if event:
                await manager.send_json({
                    'type': 'subscribed',
                    'event': event,
                    'timestamp': datetime.now().isoformat()
                }, websocket)
        
        elif message_type == 'crawler_status':
            # 爬虫状态更新
            await manager.broadcast(json.dumps({
                'type': 'crawler_status',
                'data': message.get('data', {}),
                'timestamp': datetime.now().isoformat()
            }))
    
    @staticmethod
    async def send_crawler_status(status_data: Dict[str, Any]):
        """发送爬虫状态更新"""
        await manager.send_json({
            'type': 'crawler_status',
            'data': status_data,
            'timestamp': datetime.now().isoformat()
        })
    
    @staticmethod
    async def send_notification(title: str, message: str, notification_type: str = 'info'):
        """发送通知消息"""
        await manager.send_json({
            'type': 'notification',
            'data': {
                'title': title,
                'message': message,
                'type': notification_type
            },
            'timestamp': datetime.now().isoformat()
        })
    
    @staticmethod
    async def send_progress(progress_data: Dict[str, Any]):
        """发送进度更新"""
        await manager.send_json({
            'type': 'progress',
            'data': progress_data,
            'timestamp': datetime.now().isoformat()
        })


# WebSocket事件类型
class WebSocketEvents:
    """WebSocket事件类型常量"""
    CRAWLER_STATUS = 'crawler_status'
    NOTIFICATION = 'notification'
    PROGRESS = 'progress'
    REQUEST_DATA = 'request_data'
    SEARCH_RESULT = 'search_result'
    EXPORT_PROGRESS = 'export_progress' 