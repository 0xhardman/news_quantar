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
        if event_data.get('type') == 'cast.created':
            cast = event_data.get('cast', {})
            author = cast.get('author', {})
            text = cast.get('text', '')
            logger.info(f"New cast from {author.get('username')}: {text}")
    except Exception as e:
        logger.error(f"Error processing event: {str(e)}")


if __name__ == "__main__":
    # 启动服务器
    uvicorn.run("webhook_server:app", host="0.0.0.0", port=8000, reload=True)
