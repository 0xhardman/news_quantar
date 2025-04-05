import os
import requests
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class NeynarClient:
    """Python client for the Neynar API"""
    
    BASE_URL = "https://api.neynar.com/v2/farcaster"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Neynar client with an API key
        
        Args:
            api_key: Neynar API key. If not provided, will look for NEYNAR_API_KEY in environment variables
        """
        load_dotenv()  # Load environment variables from .env file
        
        self.api_key = api_key or os.environ.get("NEYNAR_API_KEY")
        if not self.api_key:
            raise ValueError("NEYNAR_API_KEY is not set in environment variables and not provided to constructor")
        
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "api_key": self.api_key
        }
    
    def publish_webhook(self, name: str, url: str, subscription: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new webhook
        
        Args:
            name: Name of the webhook
            url: URL to send webhook events to
            subscription: Subscription configuration for the webhook
            
        Returns:
            Response from the Neynar API
        """
        endpoint = f"{self.BASE_URL}/webhook"
        
        payload = {
            "name": name,
            "url": url,
            "subscription": subscription
        }
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        return response.json()
    
    def list_webhooks(self) -> Dict[str, Any]:
        """List all webhooks
        
        Returns:
            Response from the Neynar API
        """
        endpoint = f"{self.BASE_URL}/webhook"
        
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def delete_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Delete a webhook
        
        Args:
            webhook_id: ID of the webhook to delete
            
        Returns:
            Response from the Neynar API
        """
        endpoint = f"{self.BASE_URL}/webhook/{webhook_id}"
        
        response = requests.delete(endpoint, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
    
    def get_webhook(self, webhook_id: str) -> Dict[str, Any]:
        """Get information about a webhook
        
        Args:
            webhook_id: ID of the webhook
            
        Returns:
            Response from the Neynar API
        """
        endpoint = f"{self.BASE_URL}/webhook/{webhook_id}"
        
        response = requests.get(endpoint, headers=self.headers)
        response.raise_for_status()
        
        return response.json()
