from dependency_injector.providers import Container, Factory
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.auth.application.service.jwt import JwtService
from app.user.container import UserContainer

class MainContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(
		packages=["app"],
		auto_wire=True
	)

	user = Container(UserContainer)
	jwt_service = Factory(JwtService)