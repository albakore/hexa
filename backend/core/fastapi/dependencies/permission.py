from abc import ABC, abstractmethod
from collections import defaultdict
from functools import wraps
from typing import Type

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request
from fastapi.openapi.models import APIKey, APIKeyIn
from fastapi.security.base import SecurityBase
from starlette import status
from starlette.authentication import UnauthenticatedUser


from shared.models import Permission
from core.db import session_factory
from core.exceptions.base import CustomException
from rich import print
from fastapi import APIRouter

from sqlmodel import select


class UnauthorizedException(CustomException):
	code = status.HTTP_401_UNAUTHORIZED
	error_code = "UNAUTHORIZED"
	message = ""


class InvalidPermissionActionError(CustomException):
	code = 400
	error_code = "INVALID__PERMISSION_ACTION_ERROR"
	message = "Invalid action"

	def __init__(self, message=None):
		if message:
			self.message = f"Invalid action '{message}'"


# Registro global de todos los permisos
PERMISSIONS_REGISTRY: dict[str, str] = {}


class PermissionToken:
	def __init__(self, token: str):
		self.token = token

	def __get__(self, obj, objtype=None):
		return Depends(PermissionDependency(self))  # type: ignore


class PermissionGroup:
	group: str = None  # puede sobrescribirse
	"""Nombre del grupo al que pertenecen los permisos"""

	@classmethod
	def __init_subclass__(cls):
		cls._group = cls.group or cls.__name__.lower()
		cls._permissions = {}

		for attr, desc in cls.__dict__.items():
			if (
				not attr.startswith("_")
				and isinstance(desc, str)
				and not attr.startswith("group")
			):
				token = f"{cls._group}:{attr}"
				cls._permissions[attr] = token
				PERMISSIONS_REGISTRY[token] = desc
				setattr(cls, attr, PermissionToken(token))

	@classmethod
	def list_permissions(cls):
		return [
			{"token": token, "description": desc}
			for token, desc in PERMISSIONS_REGISTRY.items()
			if token.startswith(f"{cls._group}:")
		]


def get_all_grouped_permissions() -> dict[str, list[dict[str, str]]]:
	grouped = defaultdict(list)
	for token, description in PERMISSIONS_REGISTRY.items():
		group, action = token.split(":", 1)
		grouped[group].append(
			{
				"token": token,
				"description": description,
			}
		)
	return dict(grouped)


async def sync_permissions_to_db():
	"""
	Sincroniza los permisos definidos en código con la base de datos.
	"""
	async with session_factory() as session:
		try:
			for token, description in PERMISSIONS_REGISTRY.items():
				result = await session.execute(
					select(Permission).where(Permission.token == token)
				)
				db_perm = result.scalars().first()

				if db_perm:
					if db_perm.description != description:
						db_perm.description = description
						session.add(db_perm)
						print(f"📝 Actualizado: {token}")
				else:
					session.add(
						Permission(
							group_name=token.split(":")[0],
							name=token.split(":")[1],
							token=token,
							description=description,
						)
					)
					print(f"🆕 Insertado: {token}")

			await session.commit()
			print("✅ Permisos sincronizados en base de datos")
		except Exception as e:
			print("❌ Hubo un error al sincronizar los permisos:", e)


class PermissionDependency(SecurityBase):
	def __init__(self, permission: PermissionToken):
		self.permission = permission
		self.model: APIKey = APIKey(
			**{"in": APIKeyIn.header},
			name="Authorization",
			description=f"Token de permiso **{permission.token}**",
		)
		self.scheme_name = self.__class__.__name__

	async def __call__(self, request: Request):
		if not request.user:
			raise UnauthorizedException("Not authenticated")

		if isinstance(request.user, UnauthenticatedUser):
			raise UnauthorizedException("Not authenticated")

		if self.permission.token not in request.user.permissions:
			print(f"❌ No autorizado requiere {self.permission.token}")
			raise UnauthorizedException(
				f"No autorizado, require '{self.permission.token}'"
			)


system_permission = APIRouter(tags=["System"])


@system_permission.get("/permissions")
def get_system_permissions():
	return get_all_grouped_permissions()
