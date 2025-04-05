import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, Callable, Awaitable
import json
import logging
import asyncio

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("webhook-server")


class WebhookServer:
    """Neynar Webhook 接收器服务类"""
    
    def __init__(self, callback: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None):
        """初始化 webhook 接收器服务
        
        Args:
            callback: 可选的回调函数，接收到 webhook 事件时调用
        """
        self.app = FastAPI(title="Neynar Webhook Receiver")
        self.callback = callback
        self.processed_events = set()
        
        # 注册路由
        @self.app.get("/")
        async def root():
            return {"message": "Neynar Webhook Server is running"}
        
        @self.app.post("/webhook")
        async def webhook(request: Request):
            """用于接收 Neynar webhook 事件的端点"""
            try:
                # 获取原始请求体
                body = await request.body()
                
                # 记录接收到的事件
                logger.info(f"Received webhook event: {body.decode('utf-8')}")
                
                # 解析 JSON
                try:
                    data = json.loads(body)
                    # 处理事件
                    await self.process_event(data)
                    
                    # 如果有回调函数，则调用
                    if self.callback:
                        # 添加事件ID检查
                        event_id = f"{data.get('type')}_{data.get('created_at')}"
                        if event_id not in self.processed_events:
                            self.processed_events.add(event_id)
                            logger.info(f"处理新的事件: {event_id}")
                            await self.callback(data)
                        else:
                            logger.info(f"已经处理过的事件，不再处理: {event_id}")
                    
                    return {"status": "success", "message": "Event received"}
                except json.JSONDecodeError:
                    logger.error("Failed to parse JSON")
                    raise HTTPException(status_code=400, detail="Invalid JSON")
            except Exception as e:
                logger.error(f"Error processing webhook: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def process_event(self, event_data: Dict[str, Any]):
        """处理接收到的事件
        
        Args:
            event_data: 从 Neynar 接收到的事件数据
        """
        try:
            # 检查事件类型
            event_type = event_data.get('type')
            logger.info(f"处理事件类型: {event_type}")
            
            if event_type == 'cast.created':
                # 从 data 字段获取 cast 数据
                cast_data = event_data.get('data', {})
                
                # 获取作者信息
                author = cast_data.get('author', {})
                username = author.get('username', 'unknown')
                display_name = author.get('display_name', 'unknown')
                
                # 获取 cast 文本
                text = cast_data.get('text', '')
                
                logger.info(f"新 cast 来自 {display_name} (@{username}): {text}")
        except Exception as e:
            logger.error(f"处理事件时出错: {str(e)}")
            logger.error(f"事件数据: {event_data}")
    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """启动 webhook 接收器服务
        
        Args:
            host: 服务主机地址
            port: 服务端口
        """
        uvicorn.run(self.app, host=host, port=port)


# 如果直接运行本文件，则启动服务
if __name__ == "__main__":
    server = WebhookServer()
    server.run()
