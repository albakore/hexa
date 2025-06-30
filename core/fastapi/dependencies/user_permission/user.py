from core.fastapi.dependencies.permission import (
	PermissionGroup
)


class UserTokenPermission(PermissionGroup):
    group = "user"

    read = "Lee usuarios"
    write = "Crea usuarios"
    delete = "Elimina usuarios"

class RoleTokenPermission(PermissionGroup):
    group = "role"

    read = "Lee roles"
    write = "Crea roles"
    delete = "Elimina roles"

class GroupTokenPermission(PermissionGroup):
    group = "group"

    read = "Lee grupos de permisos"
    write = "Crea grupos de permisos"
    delete = "Elimina grupos de permisos"

class PermissionTokenPermission(PermissionGroup):
    group = "permission"

    read = "Lee permission"
    write = "Crea permission"
    delete = "Elimina permission"
