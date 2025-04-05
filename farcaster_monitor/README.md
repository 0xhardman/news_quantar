# Farcaster 用户监控工具

这个简单的Python工具可以监控Farcaster上特定用户的最新发帖。

## 功能

- 通过用户名查找Farcaster用户
- 获取用户的最新发帖
- 显示发帖内容、时间、反应数据等

## 安装

1. 安装依赖包：

```bash
pip install -r requirements.txt
```

2. 确保在项目根目录的`.env`文件中设置了`NEYNAR_API_KEY`

## 使用方法

运行以下命令获取Vitalik的最新发帖：

```bash
python monitor_user.py
```

## 自定义

如果要监控其他用户，请修改`monitor_user.py`文件中的`username`变量。

## 扩展功能

- 可以修改`limit`参数获取多条发帖
- 可以添加定时任务实现持续监控
- 可以添加webhook通知功能
