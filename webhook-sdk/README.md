# Python Neynar Webhook SDK

这是一个使用 Python 实现的 Neynar Webhook SDK，用于创建和管理 Farcaster 协议的 webhooks，以及接收实时事件。

## 功能

- 创建 Neynar webhooks
- 列出现有 webhooks
- 删除 webhooks
- 接收和处理 webhook 事件

## 安装

1. 克隆仓库或复制文件到您的项目中
2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 复制 `.env.example` 为 `.env` 并填入您的 Neynar API 密钥：

```bash
cp .env.example .env
# 编辑 .env 文件，填入您的 API 密钥
```

## 使用方法

### 启动 Webhook 接收服务器

```bash
python webhook_server.py
```

服务器将在 `http://localhost:8000` 上运行，并提供 `/webhook` 端点来接收事件。

### 使用 ngrok 暴露本地服务器

为了让 Neynar 能够发送事件到您的本地服务器，您需要使用 ngrok 或类似工具：

```bash
ngrok http 8000
```

记下 ngrok 提供的公共 URL（例如 `https://abc123.ngrok.io`）。

### 创建 Webhook

```bash
python create_webhook.py --url https://your-ngrok-url.ngrok.io/webhook --name "my-webhook" --event "cast.created" --filter "\\$(ETH|eth)"
```

参数说明：
- `--url`: 接收事件的 URL（通常是您的 ngrok URL + "/webhook"）
- `--name`: webhook 的名称
- `--event`: 要订阅的事件类型（例如 cast.created, user.updated）
- `--filter`: 可选的事件过滤器（例如，只接收包含特定文本的 cast）

### 管理 Webhooks

列出所有 webhooks：

```bash
python manage_webhooks.py list
```

删除 webhook：

```bash
python manage_webhooks.py delete <webhook_id>
```

## 自定义事件处理

要自定义事件处理逻辑，请修改 `webhook_server.py` 中的 `process_event` 函数。您可以根据事件类型实现不同的业务逻辑，例如：

- 分析 cast 内容
- 触发交易
- 更新数据库
- 发送通知

## 注意事项

1. 免费的 ngrok 端点可能会受到限制，对于生产环境，建议使用付费版本或其他解决方案
2. 确保您的 API 密钥安全，不要将其提交到版本控制系统中
3. 根据您的需求调整 webhook 订阅配置

## 参考资料

- [Neynar API 文档](https://docs.neynar.com/reference/publish-webhook)
- [Farcaster 协议](https://www.farcaster.xyz/)
