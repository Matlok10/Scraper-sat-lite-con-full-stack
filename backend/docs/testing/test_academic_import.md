# Tests de Importación - Academic App

## Management Command: import_comisiones

### ✅ test_import_csv_basic
**Propósito:** Importar CSV con datos básicos.

**Input CSV:**
```csv
Período lectivo,Actividad,Comisión,Modalidad,Docente,Horario
PRIMER CUATRIMESTRE 2025,205 (PRI) - DERECHO ROMANO,0620,Presencial,GARCÍA JUAN,Lun 07:00
PRIMER CUATRIMESTRE 2025,2X8 (PRI) - DERECHO DE DAÑOS,0016,Presencial,LÓPEZ MARÍA,Mie 10:00
```

**Expectativa:**
```
✅ 2 docentes creados:
   - García Juan
   - López María

✅ 2 comisiones creadas:
   - 205-0620: DERECHO ROMANO (García Juan)
   - 2X8-0016: DERECHO DE DAÑOS (López María)
```

**Punto de fricción detectado:** ✅ NINGUNO

---

### 🧪 test_import_csv_with_dry_run
**Propósito:** Simular importación sin guardar datos.

**Comando:**
```bash
python manage.py import_comisiones archivo.csv --dry-run
```

**Expectativa:**
- Procesa el archivo.
- Muestra estadísticas.
- **NO guarda nada** en la BD.

**Caso de uso:**
```bash
# 1. Verificar el archivo primero
python manage.py import_comisiones comisiones.csv --dry-run

# 2. Si todo está bien, importar de verdad
python manage.py import_comisiones comisiones.csv
```

**Punto de fricción detectado:** ✅ NINGUNO

---

### 🔄 test_import_updates_existing_comision
**Propósito:** Actualizar comisiones existentes.

**Escenario:**
1. Ya existe: `Comision(codigo='TEST-1', docente=Docente1)`
2. CSV tiene: `TEST-1` con `Docente2`
3. Con `--update-existing`: actualiza a `Docente2`

**Comando:**
```bash
python manage.py import_comisiones actualizacion.csv --update-existing
```

**Punto de fricción detectado:** ⚠️ **POSIBLE SOBREESCRITURA NO DESEADA**

**Recomendación:**
- Agregar confirmación antes de actualizar.
- Loguear cambios en un archivo.

---

## Parsing de Actividad

### Formato 1: Con código
```
Input:  "205 (PRI) - DERECHO ROMANO"
Output: codigo="205", nombre="DERECHO ROMANO"
Código final: "205-0620"
```

### Formato 2: Sin código
```
Input:  "DERECHO ROMANO"
Output: codigo="", nombre="DERECHO ROMANO"
Código final: "0620"
```

**Regex usado:**
```python
r'^(\S+)\s+\([^)]+\)\s*-\s*(.+)$'
```

**Punto de fricción detectado:** ✅ NINGUNO
- Maneja ambos formatos correctamente.

---

## Parsing de Docente

### Formato esperado: `APELLIDO NOMBRE`

**Ejemplos:**
```
"GARCÍA JUAN"    → apellido="García", nombre="Juan"
"LÓPEZ MARÍA"    → apellido="López", nombre="María"
"PÉREZ"          → apellido="Pérez", nombre=""
```

**Lógica:**
```python
partes = nombre_completo.split()
apellido = partes[0]
nombre = ' '.join(partes[1:])
```

**Punto de fricción detectado:** ⚠️ **ASUME FORMATO ESPECÍFICO**

**Problema potencial:**
```
"Juan García Pérez" → apellido="Juan", nombre="García Pérez" ❌
Debería ser: apellido="García Pérez", nombre="Juan"
```

**Recomendación:**
- Documentar claramente el formato esperado.
- Considerar columnas separadas: `Apellido`, `Nombre`.

---

## Manejo de Duplicados

### Docentes
```python
docente, created = Docente.objects.get_or_create(
    nombre_completo__iexact=nombre_completo,
    defaults={'nombre': nombre, 'apellido': apellido}
)
```

**Comportamiento:**
- Si existe "Juan García" → reutiliza.
- Si no existe → crea nuevo.

**Punto de fricción detectado:** ⚠️ **CASE-INSENSITIVE PUEDE FALLAR**

**Problema:**
```
DB tiene: "Juan García"
CSV tiene: "Juan GARCIA"
→ Crea duplicado porque "García" != "GARCIA" en algunos casos
```

**Solución:**
```python
# Normalizar antes de buscar
nombre_completo = nombre_completo.title()
```

---

### Comisiones
```python
comision, created = Comision.objects.update_or_create(
    codigo=codigo_unico,
    defaults={...}
)
```

**Comportamiento:**
- Sin `--update-existing`: omite si existe.
- Con `--update-existing`: actualiza campos.

**Punto de fricción detectado:** ✅ NINGUNO

---

## Estadísticas de Importación

**Output del comando:**
```
📄 Leyendo CSV: archivo.csv
✅ 100 filas leídas

  👤 Docente creado: García Juan
  ✅ Comisión creada: 205-0620 - DERECHO ROMANO
  👤 Docente creado: López María
  ✅ Comisión creada: 2X8-0016 - DERECHO DE DAÑOS

============================================================
📊 RESUMEN DE IMPORTACIÓN
============================================================

👤 Docentes:
   • Creados: 45
   • Ya existentes: 10

📚 Comisiones:
   • Creadas: 120
   • Actualizadas: 0
   • Omitidas: 5

✅ Sin errores

============================================================
```

**Punto de fricción detectado:** ✅ NINGUNO

---

## Soporte de Formatos

### CSV
- Delimitador: `,` o `;` (detectado automáticamente)
- Encoding: UTF-8
- Headers requeridos: `Docente`, `Actividad`, `Comisión`

### Excel
- Formatos: `.xlsx`, `.xls`
- Requiere: `pip install openpyxl`

**Punto de fricción detectado:** ⚠️ **DEPENDENCIA OPCIONAL**

**Problema:**
```bash
python manage.py import_comisiones archivo.xlsx
# Error: openpyxl not installed
```

**Solución:**
- Documentar en README.
- O incluir en `requirements.txt`.

---

## Transacciones

```python
with transaction.atomic():
    for row in data:
        process_row(row)
    
    if dry_run:
        transaction.set_rollback(True)
```

**Comportamiento:**
- **Todo o nada**: si una fila falla, se deshace TODO.
- Protege integridad de datos.

**Punto de fricción detectado:** ⚠️ **PUEDE SER FRUSTRANTE**

**Problema:**
```
Importando 1000 filas...
Fila 999 tiene error → SE DESHACE TODO ❌
Usuario debe corregir y volver a importar las 1000
```

**Recomendación:**
- Agregar modo `--continue-on-error`.
- Loguear filas con errores para revisión manual.

---

## Casos Límite

### ✅ Comisión sin código de actividad
```csv
...
DERECHO ROMANO,0620,Presencial,GARCÍA JUAN,...
```
→ Código final: `0620` ✅

### ✅ Docente duplicado en CSV
```csv
...
205 (PRI) - DERECHO ROMANO,0620,Presencial,GARCÍA JUAN,...
2X8 (PRI) - DERECHO DE DAÑOS,0016,Presencial,GARCÍA JUAN,...
```
→ Crea 1 docente, 2 comisiones ✅

### ⚠️ CSV con encoding incorrecto
```
Input: "García" en Latin-1
Error: UnicodeDecodeError
```
**Solución:** Siempre guardar CSV como UTF-8.

---

## Resumen de Puntos de Fricción

| Feature | Estado | Fricción | Acción |
|---------|--------|----------|--------|
| Import básico | ✅ | Ninguna | - |
| Dry-run | ✅ | Ninguna | - |
| Update existing | ⚠️ | Media | Agregar confirmación |
| **Parsing nombre** | ⚠️ | **Alta** | Documentar formato |
| **Case sensitivity** | ⚠️ | **Media** | Normalizar con `.title()` |
| **Transacciones** | ⚠️ | **Media** | Agregar `--continue-on-error` |
| Excel support | ⚠️ | Baja | Documentar dependencia |

---

## Cómo Ejecutar Estos Tests

```bash
# Tests de importación
python manage.py test academic.tests.ImportComisionesCommandTest

# Test específico
python manage.py test academic.tests.ImportComisionesCommandTest.test_import_csv_basic

# Con verbose
python manage.py test academic.tests.ImportComisionesCommandTest --verbosity=2
```

---

## Mejoras Sugeridas

### 1. Modo error-tolerante
```bash
python manage.py import_comisiones archivo.csv --continue-on-error
```

### 2. Log de cambios
```bash
python manage.py import_comisiones archivo.csv --log-changes=cambios.json
```

### 3. Preview de cambios
```bash
python manage.py import_comisiones archivo.csv --preview
# Muestra: "Se crearán 10 docentes, se actualizarán 5 comisiones"
```

### 4. Validación previa
```bash
python manage.py validate_csv archivo.csv
# Verifica formato antes de importar
```
