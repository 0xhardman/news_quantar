import os
import argparse
from dotenv import load_dotenv
from neynar_client import NeynarClient

def main():
    # 加载环境变量
    load_dotenv()
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Create a Neynar webhook")
    parser.add_argument("--name", type=str, default="python-webhook", help="Name of the webhook")
    parser.add_argument("--url", type=str, required=True, help="URL to send webhook events to")
    parser.add_argument("--event", type=str, default="cast.created", 
                        help="Event type to subscribe to (e.g., cast.created, user.updated)")
    parser.add_argument("--filter", type=str, default="", 
                        help="Optional filter for the event (e.g., regex pattern for cast text)")
    
    args = parser.parse_args()
    
    # 创建 Neynar 客户端
    client = NeynarClient()
    
    # 构建订阅配置
    subscription = {}
    if args.filter:
        subscription[args.event] = {"text": args.filter}
    else:
        subscription[args.event] = {}
    
    try:
        # 创建 webhook
        response = client.publish_webhook(
            name=args.name,
            url=args.url,
            subscription=subscription
        )
        
        print("Webhook created successfully!")
        print(f"Webhook ID: {response.get('id')}")
        print(f"Name: {response.get('name')}")
        print(f"URL: {response.get('url')}")
        print(f"Subscription: {response.get('subscription')}")
    except Exception as e:
        print(f"Error creating webhook: {str(e)}")

if __name__ == "__main__":
    main()
