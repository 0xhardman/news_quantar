import argparse
from neynar_client import NeynarClient

def list_webhooks(client):
    """列出所有 webhooks"""
    try:
        response = client.list_webhooks()
        webhooks = response.get('webhooks', [])
        
        if not webhooks:
            print("No webhooks found.")
            return
        
        print(f"Found {len(webhooks)} webhooks:")
        for webhook in webhooks:
            print(f"\nID: {webhook.get('id')}")
            print(f"Name: {webhook.get('name')}")
            print(f"URL: {webhook.get('url')}")
            print(f"Subscription: {webhook.get('subscription')}")
    except Exception as e:
        print(f"Error listing webhooks: {str(e)}")

def delete_webhook(client, webhook_id):
    """删除指定 ID 的 webhook"""
    try:
        response = client.delete_webhook(webhook_id)
        print(f"Webhook {webhook_id} deleted successfully.")
    except Exception as e:
        print(f"Error deleting webhook: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Manage Neynar webhooks")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # 列出 webhooks 的子命令
    list_parser = subparsers.add_parser("list", help="List all webhooks")
    
    # 删除 webhook 的子命令
    delete_parser = subparsers.add_parser("delete", help="Delete a webhook")
    delete_parser.add_argument("webhook_id", help="ID of the webhook to delete")
    
    args = parser.parse_args()
    
    # 创建 Neynar 客户端
    client = NeynarClient()
    
    if args.command == "list":
        list_webhooks(client)
    elif args.command == "delete":
        delete_webhook(client, args.webhook_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
