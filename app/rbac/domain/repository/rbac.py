
from app.rbac.domain.repository import PermissionRepository, RoleRepository


class RBACRepository(RoleRepository, PermissionRepository):
	...