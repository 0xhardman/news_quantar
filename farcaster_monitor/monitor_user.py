import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

# 加载环境变量
load_dotenv(dotenv_path='../.env')

# 获取API密钥
NEYNAR_API_KEY = os.getenv('NEYNAR_API_KEY')
if not NEYNAR_API_KEY:
    raise ValueError("请确保在.env文件中设置了NEYNAR_API_KEY")

print(f"使用API密钥: {NEYNAR_API_KEY[:8]}...")

# Neynar API配置 - 使用V2 API
API_BASE_URL = "https://api.neynar.com/v2/farcaster"
HEADERS = {
    "accept": "application/json",
    "x-api-key": NEYNAR_API_KEY
}


def get_user_by_username(username):
    """通过用户名获取用户信息"""
    try:
        # 搜索用户
        url = f"{API_BASE_URL}/user/search?q={username}&limit=10"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

        # 搜索匹配的用户
        users = data.get('result', {}).get('users', [])
        for user in users:
            if user.get('username', '').lower() == username.lower():
                return user

        return None
    except Exception as e:
        print(f"获取用户信息失败: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"错误状态码: {e.response.status_code}")
            print(f"错误内容: {e.response.text}")
        raise


def get_user_casts(fid):
    """获取指定用户的casts"""
    try:
        url = f"{API_BASE_URL}/feed/user/popular?fid={fid}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"获取用户casts失败: {str(e)}")
        if hasattr(e, 'response') and e.response:
            print(f"错误状态码: {e.response.status_code}")
            print(f"错误内容: {e.response.text}")
        raise


def format_timestamp(timestamp_str):
    """将ISO时间格式转换为更易读的格式"""
    dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d %H:%M:%S UTC')


def display_cast(cast):
    """格式化显示发帖内容"""
    author = cast.get('author', {})
    print(f"\n{'='*50}")
    print(f"作者: {author.get('display_name')} (@{author.get('username')})")
    print(f"时间: {format_timestamp(cast.get('timestamp'))}")
    print(f"内容: {cast.get('text')}")

    # 显示嵌入内容
    embeds = cast.get('embeds', [])
    if embeds:
        print("\n嵌入内容:")
        for embed in embeds:
            if embed.get('url'):
                print(f"- 链接: {embed.get('url')}")

    # 显示反应数据
    reactions = cast.get('reactions', {})
    print(f"\n点赞: {reactions.get('likes_count', 0)} | 转发: {reactions.get('recasts_count', 0)} | 评论: {cast.get('replies', {}).get('count', 0)}")
    print(f"{'='*50}\n")


def search_vitalik():
    """搜索Vitalik的用户信息"""
    # 使用多个搜索关键词
    search_terms = ["vitalik.eth", "vitalik"]

    for term in search_terms:
        print(f"正在搜索: {term}...")
        user = get_user_by_username(term)
        if user:
            fid = user.get('fid')
            display_name = user.get('display_name', '')
            username = user.get('username', '')
            print(f"找到用户 {display_name} (@{username}), FID: {fid}")

            # 匹配 Vitalik Buterin 的用户名
            if username == "vitalik.eth" or ("vitalik" in username.lower() and "buterin" in display_name.lower()):
                return user

    return None


def main():
    # 使用正确的FID (5650，而不是5556)
    fid = 5650
    username = "vitalik.eth"
    print(f"\n正在获取用户 {username} (FID: {fid}) 的最新casts...")

    feed_data = get_user_casts(fid)
    casts = feed_data.get('casts', [])

    if not casts:
        print("未找到任何casts")
        return

    # 显示最新casts
    print("\n最新casts:")
    display_cast(casts[0])


if __name__ == "__main__":
    main()
