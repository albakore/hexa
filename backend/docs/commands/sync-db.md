# Comando sync-db

Sincroniza permisos y módulos definidos en el código con la base de datos.

## 📋 Descripción

Este comando descubre automáticamente todos los módulos y permisos definidos en el código del proyecto y los sincroniza con la base de datos. Es útil para:

- Inicializar la base de datos con permisos y módulos
- Actualizar permisos después de agregar nuevos
- Actualizar módulos después de cambios en configuración

## 🚀 Uso

### Sincronizar todo (permisos y módulos)

```bash
uv run hexa sync-db
```

### Solo sincronizar permisos

```bash
uv run hexa sync-db --no-modules
```

### Solo sincronizar módulos

```bash
uv run hexa sync-db --no-permissions
```

## 📊 Salida esperada

```
🔄 Iniciando sincronización con la base de datos...
============================================================

📦 Descubriendo módulos...
✅ Módulos descubiertos

📦 Cargando configuraciones de módulos...
✅ Configuraciones cargadas

🔐 Sincronizando permisos...
------------------------------------------------------------
🆕 Insertado: user:read
🆕 Insertado: user:write
🆕 Insertado: user:create
🆕 Insertado: user:delete
🆕 Insertado: invoices:read
🆕 Insertado: invoices:write
🆕 Insertado: invoices:create
🆕 Insertado: invoices:emit
✅ Permisos sincronizados en base de datos

📚 Sincronizando módulos...
------------------------------------------------------------
🆕 Insertado modulo: Users
🆕 Insertado modulo: Invoicing
🆕 Insertado modulo: YiqiERP
✅ Modulos sincronizados en base de datos

============================================================
✨ Sincronización completada exitosamente
```

## 🔧 Cómo funciona

1. **Limpia registros**: Borra ModuleRegistry y service_locator para empezar limpio
2. **Descubre módulos**: Busca todos los módulos en la carpeta `modules/`
3. **Carga configuraciones**: Lee archivos `setup.py` de cada módulo
4. **Sincroniza permisos**: Compara permisos en código vs. base de datos
   - Inserta nuevos permisos
   - Actualiza descripciones de permisos existentes
5. **Sincroniza módulos**: Compara módulos en código vs. base de datos
   - Inserta nuevos módulos
   - Actualiza nombres y descripciones de módulos existentes

## 📝 Definir permisos

Los permisos se definen usando `PermissionGroup`:

```python
# modules/user/permissions.py
from core.fastapi.dependencies.permission import PermissionGroup

class UserPermissions(PermissionGroup):
    group = "user"

    read = "Ver usuarios"
    write = "Escribir usuarios"
    create = "Crear usuarios"
    delete = "Eliminar usuarios"
```

Esto genera automáticamente los tokens:
- `user:read`
- `user:write`
- `user:create`
- `user:delete`

## 📝 Definir módulos

Los módulos se definen usando `ModuleSetup`:

```python
# modules/user/setup.py
from core.config.modules import ModuleSetup

class UserModule(ModuleSetup):
    name = "Users"
    token = "users"
    description = "Gestión de usuarios del sistema"
```

## 🔄 Cuándo ejecutar

### Primera instalación
Después de crear las migraciones de Alembic:

```bash
# 1. Aplicar migraciones
alembic upgrade head

# 2. Sincronizar permisos y módulos
uv run hexa sync-db
```

### Después de agregar nuevos permisos
Cada vez que agregas nuevos permisos a un `PermissionGroup`:

```bash
uv run hexa sync-db
```

### Después de modificar módulos
Cada vez que modificas un `ModuleSetup`:

```bash
uv run hexa sync-db
```

### En desarrollo
Si trabajas con permisos frecuentemente, puedes agregarlo a tu flujo:

```bash
# Ver cambios y sincronizar
uv run hexa sync-db
```

## ⚠️ Notas importantes

1. **No elimina datos**: El comando solo inserta y actualiza, nunca elimina permisos o módulos de la base de datos
2. **Idempotente**: Puedes ejecutarlo múltiples veces sin problemas
3. **Requiere base de datos**: Asegúrate de que las migraciones de Alembic estén aplicadas
4. **Descubrimiento automático**: No necesitas importar manualmente los módulos

## 🐛 Troubleshooting

### Error: "table doesn't exist"
```bash
# Aplicar migraciones primero
alembic upgrade head
```

### No se registran permisos
Verifica que:
- La clase hereda de `PermissionGroup`
- Los permisos son atributos de clase con valores string
- El archivo está en un módulo descubierto

### No se registran módulos
Verifica que:
- Existe el archivo `modules/<modulo>/setup.py`
- La clase hereda de `ModuleSetup`
- Tiene definidos `name`, `token` y `description`

## 📚 Ver también

- [Sistema de permisos](../core/04-permissions-decorator.md)
- [Estructura de módulos](../architecture/02-project-structure.md)
- [CLI Commands](../development/03-cli-commands.md)
