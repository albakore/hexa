#!/bin/bash

# Script para aplicar las mejoras de Docker Compose en modo desarrollo
# Uso: ./apply_docker_improvements.sh

set -e

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Docker Compose Development - Mejoras Automáticas   ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "compose.dev.yaml" ]; then
    echo -e "${RED}❌ Error: No se encontró compose.dev.yaml${NC}"
    echo "   Ejecuta este script desde el directorio backend/"
    exit 1
fi

# Paso 1: Backup del archivo original
echo -e "${YELLOW}📦 Paso 1: Creando backup del compose.dev.yaml original...${NC}"
if [ ! -f "compose.dev.yaml.backup" ]; then
    cp compose.dev.yaml compose.dev.yaml.backup
    echo -e "${GREEN}   ✅ Backup creado: compose.dev.yaml.backup${NC}"
else
    echo -e "${YELLOW}   ⚠️  Ya existe compose.dev.yaml.backup (omitido)${NC}"
fi
echo ""

# Paso 2: Instalar watchfiles
echo -e "${YELLOW}📦 Paso 2: Verificando e instalando watchfiles...${NC}"
if ! grep -q "watchfiles" pyproject.toml; then
    echo -e "${BLUE}   Agregando watchfiles a dependencias de desarrollo...${NC}"
    uv add --dev watchfiles
    echo -e "${GREEN}   ✅ watchfiles agregado${NC}"
else
    echo -e "${GREEN}   ✅ watchfiles ya está instalado${NC}"
fi
echo ""

# Paso 3: Aplicar compose optimizado
echo -e "${YELLOW}📦 Paso 3: Aplicando configuración optimizada...${NC}"
if [ -f "compose.dev.yaml.optimized" ]; then
    cp compose.dev.yaml.optimized compose.dev.yaml
    echo -e "${GREEN}   ✅ compose.dev.yaml actualizado${NC}"
else
    echo -e "${RED}   ❌ No se encontró compose.dev.yaml.optimized${NC}"
    exit 1
fi
echo ""

# Paso 4: Detener contenedores actuales
echo -e "${YELLOW}📦 Paso 4: Deteniendo contenedores actuales...${NC}"
docker compose -f compose.dev.yaml down 2>/dev/null || true
echo -e "${GREEN}   ✅ Contenedores detenidos${NC}"
echo ""

# Paso 5: Rebuild de imágenes
echo -e "${YELLOW}📦 Paso 5: Rebuilding imágenes de Docker...${NC}"
echo -e "${BLUE}   Esto puede tardar unos minutos...${NC}"
docker compose -f compose.dev.yaml build --no-cache
echo -e "${GREEN}   ✅ Imágenes rebuildeadas${NC}"
echo ""

# Paso 6: Mostrar resumen
echo -e "${GREEN}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              ✅ Mejoras Aplicadas Exitosamente         ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📋 Cambios aplicados:${NC}"
echo "   ✅ Celery worker con auto-reload (watchfiles)"
echo "   ✅ Health checks para Redis y RabbitMQ"
echo "   ✅ Volumen persistente para RabbitMQ"
echo "   ✅ Patrones de ignore optimizados"
echo "   ✅ Variables de entorno optimizadas"
echo "   ✅ Imágenes Alpine más ligeras"
echo "   ✅ Restart policies configuradas"
echo ""
echo -e "${BLUE}🚀 Próximos pasos:${NC}"
echo ""
echo -e "   1. Iniciar en modo watch:"
echo -e "      ${GREEN}docker compose -f compose.dev.yaml watch${NC}"
echo ""
echo -e "   2. Ver logs:"
echo -e "      ${GREEN}docker compose -f compose.dev.yaml logs -f${NC}"
echo ""
echo -e "   3. Verificar health checks:"
echo -e "      ${GREEN}docker compose -f compose.dev.yaml ps${NC}"
echo ""
echo -e "   4. Probar auto-reload:"
echo -e "      ${GREEN}# Modificar un archivo Python y ver los logs${NC}"
echo ""
echo -e "${YELLOW}💡 Tip:${NC} Para revertir cambios, usa:"
echo -e "   ${GREEN}cp compose.dev.yaml.backup compose.dev.yaml${NC}"
echo ""
echo -e "${BLUE}📚 Documentación completa: ${GREEN}DOCKER_COMPOSE_ANALYSIS.md${NC}"
echo ""
