from core.fastapi.dependencies.permission import PermissionGroup


class ModuleTaxesPermission(PermissionGroup):
	group = "taxes"

	read = "Lee Impuestos"
	write = "Crea Impuestos"
	update = "Modifica Impuestos"
	delete = "Elimina Impuestos"
