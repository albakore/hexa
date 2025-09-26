from modules.rbac.domain.repository import PermissionRepository, RoleRepository


class RBACRepository(RoleRepository, PermissionRepository): ...
