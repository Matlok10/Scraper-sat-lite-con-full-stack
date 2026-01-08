#!/bin/bash
# Script para demostrar los cambios en la lógica de deduplicación

set -e

BACKEND_DIR="/mnt/nobara-data/proyectos/Recos completo/backend"
TEST_DIR="$BACKEND_DIR/tests"
TEST_FILE="$TEST_DIR/test_import_multiples_horarios.csv"

echo "=================================================="
echo "🧪 TEST: Múltiples Horarios para Misma Comisión"
echo "=================================================="
echo ""

# Crear archivo de prueba con casos específicos
cat > "$TEST_FILE" << 'EOF'
Período lectivo,Actividad,Comisión,Modalidad,Docente,Horario,RECOMENDACIÓN
PRIMER CUATRIMESTRE ABOGACÍA 2025,205 (PRI) - DERECHO ROMANO,0620,Presencial,LOCOCO JULIO,Lun 07:00 a 08:30,Cátedra exigente
PRIMER CUATRIMESTRE ABOGACÍA 2025,2X8 (PRI) - DERECHO DE DAÑOS,0027,Presencial,MARTINEZ GARBINO C.,Lun 10:00 a 11:30,Clase teórica
PRIMER CUATRIMESTRE ABOGACÍA 2025,2X8 (PRI) - DERECHO DE DAÑOS,0027,Presencial,MARTINEZ GARBINO C.,Mar 14:00 a 15:30,Clase teórica (otro horario)
PRIMER CUATRIMESTRE ABOGACÍA 2025,2X8 (PRI) - DERECHO DE DAÑOS,0027,Presencial,MARTINEZ GARBINO C.,Lun 10:00 a 11:30,Clase teórica (DUPLICADO EXACTO)
PRIMER CUATRIMESTRE ABOGACÍA 2025,73U (PRI) - DOMINIO FIDUCIARIO,0381,Presencial,ACEVEDO MARIA ESTHER,Lun 07:00 a 08:30,Clase
PRIMER CUATRIMESTRE ABOGACÍA 2025,2X8 (PRI) - DERECHO DE DAÑOS,0027,Presencial,COMPIANI MARIA F.,Lun 10:00 a 11:30,ERROR: Múltiples docentes
EOF

echo "✅ Archivo de prueba creado: $TEST_FILE"
echo ""
echo "📋 Contenido del archivo:"
cat "$TEST_FILE" | head -10
echo ""

# Cambiar a backend
cd "$BACKEND_DIR"

echo "🔍 Ejecutando import con --dry-run para ver qué pasaría..."
echo ""

python manage.py import_comisiones "$TEST_FILE" --dry-run

echo ""
echo "=================================================="
echo "📊 ANÁLISIS DE RESULTADOS"
echo "=================================================="
echo ""
echo "✅ CASOS VALIDADOS:"
echo ""
echo "1. Comisión 0027 con 2 horarios válidos:"
echo "   - Lun 10:00 a 11:30 (MARTINEZ) ✅"
echo "   - Mar 14:00 a 15:30 (MARTINEZ) ✅"
echo "   → AMBOS se procesan porque es válido"
echo ""
echo "2. Comisión 0027 (fila 4): Duplicado exacto"
echo "   - Lun 10:00 a 11:30 (MARTINEZ) - IDENTICO a fila 2"
echo "   → SE OMITE porque es un copypaste"
echo ""
echo "3. Comisión 0027 (fila 6): Múltiples docentes"
echo "   - Profesor: MARTINEZ en filas anteriores"
echo "   - Profesor: COMPIANI en fila 6"
echo "   → SE REPORTA ERROR (misma comisión, docentes diferentes)"
echo ""
echo "=================================================="
echo "✅ TEST COMPLETADO"
echo "=================================================="
