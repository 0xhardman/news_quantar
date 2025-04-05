# Python Neynar Webhook SDK

This is a Python implementation of the Neynar Webhook SDK for creating and managing webhooks for the Farcaster protocol, as well as receiving real-time events.

## Features

- Create Neynar webhooks
- List existing webhooks
- Delete webhooks
- Receive and process webhook events

## Installation

1. Clone the repository or copy the files into your project
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and add your Neynar API key:

```bash
cp .env.example .env
# Edit the .env file and add your API key
```

## Usage

### Start the Webhook Receiver Server

```bash
python webhook_server.py
```

The server will run at `http://localhost:8000` and provide a `/webhook` endpoint to receive events.

### Expose Your Local Server with ngrok

To allow Neynar to send events to your local server, you need to use ngrok or a similar tool:

```bash
ngrok http 8000
```

Note the public URL provided by ngrok (e.g., `https://abc123.ngrok.io`).

### Create a Webhook

```bash
python create_webhook.py --url https://your-ngrok-url.ngrok.io/webhook --name "my-webhook" --event "cast.created" --filter "\\$(ETH|eth)"
```

Parameters:
- `--url`: URL to receive events (typically your ngrok URL + "/webhook")
- `--name`: name of the webhook
- `--event`: type of event to subscribe to (e.g., cast.created, user.updated)
- `--filter`: optional event filter (e.g., only receive casts containing specific text)

### Manage Webhooks

List all webhooks:

```bash
python manage_webhooks.py list
```

Delete a webhook:

```bash
python manage_webhooks.py delete <webhook_id>
```

## Customize Event Handling

To customize event handling logic, modify the `process_event` function in `webhook_server.py`. You can implement different business logic based on event types, such as:

- Analyzing cast content
- Triggering transactions
- Updating databases
- Sending notifications

## Notes

1. Free ngrok endpoints may have limitations; for production environments, consider using the paid version or other solutions
2. Keep your API key secure and don't commit it to version control systems
3. Adjust webhook subscription configuration according to your needs

## References

- [Neynar API Documentation](https://docs.neynar.com/reference/publish-webhook)
- [Farcaster Protocol](https://www.farcaster.xyz/)
