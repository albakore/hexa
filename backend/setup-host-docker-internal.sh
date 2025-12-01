#!/bin/bash

# Script para configurar host.docker.internal en Ubuntu
# Uso: chmod +x setup-host-docker-internal.sh
# sudo ./setup-host-docker-internal.sh [IP_OPCIONAL]

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que se ejecuta como root
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}Este script debe ejecutarse como root o con sudo${NC}"
   exit 1
fi

# IP a usar (por defecto 127.0.0.1)
TARGET_IP="${1:-127.0.0.1}"

echo -e "${YELLOW}Configurando host.docker.internal...${NC}"

# Nombre del host
HOST_NAME="host.docker.internal"

# Verificar si ya existe la entrada
if grep -q "$HOST_NAME" /etc/hosts; then
    echo -e "${YELLOW}La entrada para $HOST_NAME ya existe en /etc/hosts${NC}"
    echo -e "${YELLOW}Actualizando...${NC}"
    
    # Eliminar la entrada anterior
    sed -i "/$HOST_NAME/d" /etc/hosts
fi

# Agregar la nueva entrada
echo "$TARGET_IP   $HOST_NAME" >> /etc/hosts

echo -e "${GREEN}✓ Configuración completada${NC}"
echo -e "${GREEN}✓ $HOST_NAME apunta a $TARGET_IP${NC}"

# Verificar la configuración
echo -e "\n${YELLOW}Verificando configuración...${NC}"
if getent hosts $HOST_NAME > /dev/null; then
    echo -e "${GREEN}✓ Host configurado correctamente:${NC}"
    getent hosts $HOST_NAME
else
    echo -e "${RED}✗ Error al verificar la configuración${NC}"
    exit 1
fi

# Probar conectividad
echo -e "\n${YELLOW}Probando conectividad...${NC}"
if ping -c 2 $HOST_NAME > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Ping exitoso a $HOST_NAME${NC}"
else
    echo -e "${YELLOW}⚠ No se pudo hacer ping (esto puede ser normal si el firewall bloquea ICMP)${NC}"
fi

echo -e "\n${GREEN}Configuración finalizada. Ahora puedes usar $HOST_NAME en tus variables de entorno.${NC}"