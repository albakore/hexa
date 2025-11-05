from abc import ABC, abstractmethod


class SenderProviderPort(ABC):

	@abstractmethod
	async def send(self, notification: dict) -> None:
		...

	# @abstractmethod
	# async def send(self, from_: str | None, to: list[str], subject: str, body: str | dict) -> None:
	# 	...