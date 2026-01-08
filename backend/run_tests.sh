#!/bin/bash
# Script para ejecutar todos los tests del proyecto con venv activado

echo "=========================================="
echo "EJECUTANDO TESTS DEL PROYECTO"
echo "=========================================="

# Activar venv
source ../venv/bin/activate

echo ""
echo "Entorno Python activado:"
python --version
echo ""

# Ejecutar tests por app
echo "=========================================="
echo "1. TESTS DE USERS APP"
echo "=========================================="
python manage.py test tests.test_users --verbosity=2

echo ""
echo "=========================================="
echo "2. TESTS DE MODELS"
echo "=========================================="
python manage.py test tests.test_models --verbosity=2

echo ""
echo "=========================================="
echo "3. TESTS DE API"
echo "=========================================="
python manage.py test tests.test_api --verbosity=2

echo ""
echo "=========================================="
echo "4. TESTS DE USERS (en app)"
echo "=========================================="
python manage.py test users.tests --verbosity=2

echo ""
echo "=========================================="
echo "RESUMEN: TODOS LOS TESTS"
echo "=========================================="
python manage.py test --verbosity=1

echo ""
echo "=========================================="
echo "TESTS COMPLETADOS"
echo "=========================================="
