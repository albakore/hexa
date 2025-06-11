from dependency_injector.providers import Container, Factory
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.auth.container import AuthContainer
from app.user.container import UserContainer

class MainContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(
		packages=["app"],
		auto_wire=True
	)

	user = Container(UserContainer)
	auth = Container(AuthContainer)