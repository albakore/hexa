from abc import ABC, abstractmethod
from typing import Any, Dict, List, Callable
from dataclasses import dataclass
from datetime import datetime


@dataclass
class DomainEvent:
	"""Evento de dominio base"""

	event_type: str
	data: Dict[str, Any]
	timestamp: datetime
	module_source: str


class EventHandler(ABC):
	"""Interface para manejadores de eventos"""

	@abstractmethod
	def handle(self, event: DomainEvent) -> None:
		"""Maneja un evento de dominio"""
		pass


class EventBus:
	"""Bus de eventos para comunicación entre módulos"""

	def __init__(self):
		self._handlers: Dict[str, List[EventHandler]] = {}

	def subscribe(self, event_type: str, handler: EventHandler) -> None:
		"""Suscribe un handler a un tipo de evento"""
		if event_type not in self._handlers:
			self._handlers[event_type] = []
		self._handlers[event_type].append(handler)

	def publish(self, event: DomainEvent) -> None:
		"""Publica un evento a todos los handlers suscritos"""
		handlers = self._handlers.get(event.event_type, [])
		for handler in handlers:
			try:
				handler.handle(event)
			except Exception as e:
				# Log error but don't stop other handlers
				print(f"Error handling event {event.event_type}: {e}")


# Instancia global del bus de eventos
event_bus = EventBus()
