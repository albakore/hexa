from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class UseCase(ABC):
	@abstractmethod
	async def __call__(self): ...


class CreateInvoice(UseCase):
	async def __call__(self):
		raise NotImplementedError


class GetInvoicesByCliendId(UseCase):
	async def __call__(self):
		raise NotImplementedError


@dataclass
class InvoiceUseCaseFactory:
	def __post_init__(self): ...
