"""
FastAPI Dependencies usando dependency-injector
"""

from dependency_injector.wiring import inject
from shared.interfaces.service_locator import service_locator


def get_user_service():
	return service_locator.get_service("user_service")


def get_auth_service():
	return service_locator.get_service("auth_service")


def get_jwt_service():
	return service_locator.get_service("jwt_service")


@inject
def get_role_service():
	return service_locator.get_service("role_service")


def get_permission_service():
	return service_locator.get_service("permission_service")


def get_currency_service():
	return service_locator.get_service("currency_service")


def get_provider_service():
	return service_locator.get_service("provider_service")


def get_draft_invoice_service():
	return service_locator.get_service("draft_invoice_service")


def get_yiqi_service():
	return service_locator.get_service("yiqi_service")


def get_app_module_service():
	return service_locator.get_service("app_module_service")


def get_user_relationship_service():
	return service_locator.get_service("user_relationship_service")
