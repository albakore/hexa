from dependency_injector.providers import Container, Factory
from dependency_injector.containers import DeclarativeContainer, WiringConfiguration

from app.auth.container import AuthContainer
from app.rbac.container import RBACContainer
from app.user.container import UserContainer

class MainContainer(DeclarativeContainer):
	wiring_config = WiringConfiguration(
		packages=["app"],
		auto_wire=True
	)

	rbac = Container(RBACContainer)
	user = Container(UserContainer)
	auth = Container(AuthContainer)