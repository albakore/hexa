#!/bin/bash

# Script para ejecutar tests del proyecto con diferentes opciones
# Uso: ./run_tests.sh [opción]

set -e

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Función para mostrar ayuda
show_help() {
    echo -e "${BLUE}=== Test Runner para Fast Hexagonal ===${NC}"
    echo ""
    echo "Uso: ./run_tests.sh [opción]"
    echo ""
    echo "Opciones:"
    echo "  all              - Ejecutar todos los tests"
    echo "  unit             - Solo tests unitarios"
    echo "  integration      - Solo tests de integración"
    echo "  module <nombre>  - Tests de un módulo específico"
    echo "  coverage         - Tests con reporte de cobertura"
    echo "  quick            - Tests rápidos (solo unitarios, sin slow)"
    echo "  verbose          - Tests con output detallado"
    echo "  help             - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  ./run_tests.sh all"
    echo "  ./run_tests.sh unit"
    echo "  ./run_tests.sh module invoicing"
    echo "  ./run_tests.sh coverage"
}

# Función para ejecutar todos los tests
run_all() {
    echo -e "${GREEN}Ejecutando todos los tests...${NC}"
    uv run --active pytest -v
}

# Función para ejecutar solo tests unitarios
run_unit() {
    echo -e "${GREEN}Ejecutando tests unitarios...${NC}"
    pytest -v -m unit
}

# Función para ejecutar solo tests de integración
run_integration() {
    echo -e "${GREEN}Ejecutando tests de integración...${NC}"
    pytest -v -m integration
}

# Función para ejecutar tests de un módulo específico
run_module() {
    if [ -z "$1" ]; then
        echo -e "${RED}Error: Debes especificar el nombre del módulo${NC}"
        echo "Ejemplo: ./run_tests.sh module invoicing"
        exit 1
    fi

    MODULE_PATH="modules/$1/test"

    if [ ! -d "$MODULE_PATH" ]; then
        echo -e "${RED}Error: No existe el directorio de tests para el módulo '$1'${NC}"
        echo "Ruta buscada: $MODULE_PATH"
        exit 1
    fi

    echo -e "${GREEN}Ejecutando tests del módulo $1...${NC}"
    pytest -v "$MODULE_PATH"
}

# Función para ejecutar tests con coverage
run_coverage() {
    echo -e "${GREEN}Ejecutando tests con cobertura...${NC}"
    pytest --cov=modules --cov-report=html --cov-report=term -v
    echo ""
    echo -e "${YELLOW}Reporte HTML generado en: htmlcov/index.html${NC}"
}

# Función para ejecutar tests rápidos
run_quick() {
    echo -e "${GREEN}Ejecutando tests rápidos (unitarios, sin slow)...${NC}"
    pytest -v -m "unit and not slow"
}

# Función para ejecutar tests con output detallado
run_verbose() {
    echo -e "${GREEN}Ejecutando tests con output detallado...${NC}"
    pytest -vv -s
}

# Main script
case "${1:-help}" in
    all)
        run_all
        ;;
    unit)
        run_unit
        ;;
    integration)
        run_integration
        ;;
    module)
        run_module "$2"
        ;;
    coverage)
        run_coverage
        ;;
    quick)
        run_quick
        ;;
    verbose)
        run_verbose
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Opción no reconocida: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Ejecución completada${NC}"
