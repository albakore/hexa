# 🔧 Fix: Error de Redis - RDB Format Version 12

## 🚨 Problema Identificado

```
Can't handle RDB format version 12
Fatal error loading the DB: Invalid argument. Exiting.
```

### Causa

Redis 6.2 no puede leer archivos RDB (Redis Database) creados con Redis 7+.
El volumen de Redis tiene datos de una versión más nueva.

---

## ✅ Soluciones

### Opción 1: Limpiar Volumen de Redis (Recomendado para Dev)

**⚠️ ADVERTENCIA:** Esto borrará todos los datos de Redis (colas, caché, etc.)

```bash
cd backend

# Detener servicios
docker compose -f compose.dev.yaml down

# Eliminar volumen de Redis
docker volume rm backend_redis

# Reiniciar servicios
docker compose -f compose.dev.yaml up -d
```

**Ventajas:**
- ✅ Rápido y simple
- ✅ Solución permanente
- ✅ Redis 6.2 inicia limpio

**Desventajas:**
- ❌ Pierdes datos en Redis (acceptable en desarrollo)

---

### Opción 2: Actualizar a Redis 7 (Recomendado para el Futuro)

Editar `compose.dev.yaml`:

```yaml
redis:
  container_name: redis
  image: redis:7-alpine  # ← Cambiar de 6.2-alpine a 7-alpine
  restart: always
  # ... resto igual
```

Luego:

```bash
cd backend

# Detener servicios
docker compose -f compose.dev.yaml down

# Pull nueva imagen
docker compose -f compose.dev.yaml pull redis

# Reiniciar
docker compose -f compose.dev.yaml up -d
```

**Ventajas:**
- ✅ Mantiene compatibilidad con datos existentes
- ✅ Versión más reciente de Redis
- ✅ Mejor performance

**Desventajas:**
- ⚠️ Requiere cambio en compose

---

### Opción 3: Migrar Datos (Si necesitas preservar datos)

Si tienes datos importantes en Redis:

```bash
cd backend

# 1. Backup del volumen actual
docker run --rm -v backend_redis:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup.tar.gz -C /data .

# 2. Actualizar imagen a Redis 7
# (editar compose.dev.yaml como en Opción 2)

# 3. Detener y limpiar
docker compose -f compose.dev.yaml down
docker volume rm backend_redis

# 4. Crear nuevo volumen y restaurar
docker compose -f compose.dev.yaml up -d redis
sleep 5
docker compose -f compose.dev.yaml down

# 5. Restaurar backup
docker run --rm -v backend_redis:/data -v $(pwd):/backup alpine tar xzf /backup/redis-backup.tar.gz -C /data

# 6. Reiniciar
docker compose -f compose.dev.yaml up -d
```

---

## 🎯 Recomendación

Para tu proyecto en **desarrollo**, usa **Opción 1** (limpiar volumen):

```bash
# Comando único
docker compose -f compose.dev.yaml down && \
docker volume rm backend_redis && \
docker compose -f compose.dev.yaml up -d
```

Luego, para evitar este problema en el futuro, actualiza a Redis 7 (Opción 2).

---

## 🔍 Verificación

Después de aplicar la solución:

```bash
# Ver estado
docker compose -f compose.dev.yaml ps

# Deberías ver:
# redis       Up (healthy)
```

```bash
# Ver logs
docker compose -f compose.dev.yaml logs redis

# Deberías ver:
# Ready to accept connections
```

```bash
# Probar conexión
docker compose -f compose.dev.yaml exec redis redis-cli -a eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81 ping

# Deberías ver:
# PONG
```

---

## 📝 Fix del Healthcheck (Ya Aplicado)

También arreglé el healthcheck de Redis para que use la contraseña correctamente:

```yaml
redis:
  healthcheck:
    test: ["CMD", "redis-cli", "-a", "eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81", "ping"]
    interval: 10s
    timeout: 3s
    retries: 5
```

Esto evita el error:
```
(error) NOAUTH Authentication required.
```

---

## 🚀 Aplicar Fix Rápido

```bash
cd /home/albakore/Documents/Repositories/fast-hexagonal/backend

# Fix completo en un comando
docker compose -f compose.dev.yaml down && \
docker volume rm backend_redis 2>/dev/null || true && \
docker compose -f compose.dev.yaml up -d && \
echo "✅ Redis arreglado! Esperando 10 segundos..." && \
sleep 10 && \
docker compose -f compose.dev.yaml ps redis
```

---

**Creado:** 2025-10-24
**Estado:** ✅ Healthcheck corregido en compose.dev.yaml
**Acción requerida:** Limpiar volumen de Redis
