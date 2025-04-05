import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import json
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("webhook-server")

app = FastAPI(title="Neynar Webhook Receiver")


class WebhookEvent(BaseModel):
    """Pydantic model for webhook events"""
    event_type: Optional[str] = None
    data: Optional[Dict[str, Any]] = None


@app.get("/")
async def root():
    return {"message": "Neynar Webhook Server is running"}


@app.post("/webhook")
async def webhook(request: Request):
    """Endpoint to receive webhook events from Neynar"""
    try:
        # 获取原始请求体
        body = await request.body()
        
        # 记录接收到的事件
        logger.info(f"Received webhook event: {body.decode('utf-8')}")
        
        # 解析 JSON
        try:
            data = json.loads(body)
            # 这里可以根据事件类型处理不同的逻辑
            # 例如：if data.get('event_type') == 'cast.created':
            
            # 处理事件的示例
            process_event(data)
            
            return {"status": "success", "message": "Event received"}
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON")
            raise HTTPException(status_code=400, detail="Invalid JSON")
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


def process_event(event_data: Dict[str, Any]):
    """处理接收到的事件
    
    这里可以实现您的业务逻辑，例如：
    - 分析 cast 内容
    - 触发交易
    - 更新数据库
    - 发送通知
    
    Args:
        event_data: 从 Neynar 接收到的事件数据
    """
    # 示例：提取 cast 内容并打印
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
            
            # 这里可以添加您的业务逻辑，例如检测特定关键词并触发操作
            if '$(ETH)' in text or '$(eth)' in text or 'ETH' in text or 'eth' in text:
                logger.info(f"检测到 ETH 相关内容: {text}")
                # 在这里可以触发交易或其他操作
    except Exception as e:
        logger.error(f"处理事件时出错: {str(e)}")
        logger.error(f"事件数据: {event_data}")


if __name__ == "__main__":
    # 启动服务器
    uvicorn.run("webhook_server:app", host="0.0.0.0", port=8000, reload=True)
