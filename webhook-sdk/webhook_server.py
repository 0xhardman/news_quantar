import uvicorn
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, Callable, Awaitable
import json
import logging
import asyncio

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("webhook-server")


class WebhookServer:
    """Neynar Webhook Receiver Service Class"""
    
    def __init__(self, callback: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None):
        """Initialize webhook receiver service
        
        Args:
            callback: Optional callback function to call when webhook events are received
        """
        self.app = FastAPI(title="Neynar Webhook Receiver")
        self.callback = callback
        self.processed_events = set()
        
        # Register routes
        @self.app.get("/")
        async def root():
            return {"message": "Neynar Webhook Server is running"}
        
        @self.app.post("/webhook")
        async def webhook(request: Request):
            """Endpoint for receiving Neynar webhook events"""
            try:
                # Get raw request body
                body = await request.body()
                
                # Log received event
                logger.info(f"Received webhook event: {body.decode('utf-8')}")
                
                # Parse JSON
                try:
                    data = json.loads(body)
                    # Process event
                    await self.process_event(data)
                    
                    # Call callback function if provided
                    if self.callback:
                        # Add event ID check
                        event_id = f"{data.get('type')}_{data.get('created_at')}"
                        if event_id not in self.processed_events:
                            self.processed_events.add(event_id)
                            logger.info(f"Processing new event: {event_id}")
                            await self.callback(data)
                        else:
                            logger.info(f"Already processed event, skipping: {event_id}")
                    
                    return {"status": "success", "message": "Event received"}
                except json.JSONDecodeError:
                    logger.error("Failed to parse JSON")
                    raise HTTPException(status_code=400, detail="Invalid JSON")
            except Exception as e:
                logger.error(f"Error processing webhook: {str(e)}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def process_event(self, event_data: Dict[str, Any]):
        """Process received events
        
        Args:
            event_data: Event data received from Neynar
        """
        try:
            # Check event type
            event_type = event_data.get('type')
            logger.info(f"Processing event type: {event_type}")
            
            if event_type == 'cast.created':
                # Get cast data from data field
                cast_data = event_data.get('data', {})
                
                # Get author information
                author = cast_data.get('author', {})
                username = author.get('username', 'unknown')
                display_name = author.get('display_name', 'unknown')
                
                # Get cast text
                text = cast_data.get('text', '')
                
                logger.info(f"New cast from {display_name} (@{username}): {text}")
        except Exception as e:
            logger.error(f"Error processing event: {str(e)}")
            logger.error(f"Event data: {event_data}")
    
    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Start webhook receiver service
        
        Args:
            host: Service host address
            port: Service port
        """
        uvicorn.run(self.app, host=host, port=port)


# If this file is run directly, start the service
if __name__ == "__main__":
    server = WebhookServer()
    server.run()
