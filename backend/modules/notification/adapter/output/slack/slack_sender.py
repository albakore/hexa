import httpx

from modules.notification.domain.repository.sender_provider import SenderProviderPort


class SlackSender(SenderProviderPort):
	def __init__(self, webhook_url: str, w: str):
		self.webhook_url = webhook_url

	async def send(self, notification: dict) -> None:
		if isinstance(notification['body'], dict):
			payload = notification['body']
		if isinstance(notification['body'], str):
			payload = {
				"blocks": [
					{
						"type": "section",
						"text": {"type": "mrkdwn", "text": f"""{notification['body']}"""},
					},
				]
			}

		async with httpx.AsyncClient() as client:
			headers = {"Content-type": "application/json"}
			response = await client.post(
				self.webhook_url, json=payload, headers=headers
			)
			if response.status_code != 200:
				print(
					f"Slack respondió con error: {response.status_code} - {response.text}"
				)
