# 📥 Explicación Detallada: Sistema de Importación

## 🎯 Objetivo del Sistema

Importar **miles de comisiones** desde archivos Excel/CSV de forma segura, manejando duplicados y errores de usuario automáticamente.

---

## 🔄 Flujo Completo de Importación

```
┌─────────────────────────────────────────────────────────────┐
│  USUARIO: Sube archivo.xlsx o archivo.csv                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 1: Lectura del Archivo                               │
│  ───────────────────────────────────────────────────────    │
│  • Detecta formato (CSV o Excel)                            │
│  • Lee todas las filas                                      │
│  • Convierte a lista de diccionarios                        │
│                                                              │
│  Ejemplo: 500 filas leídas ✅                               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 2: Transacción Atómica (TODO O NADA)                 │
│  ───────────────────────────────────────────────────────    │
│  transaction.atomic():                                      │
│      ├─ Procesa fila 1                                      │
│      ├─ Procesa fila 2                                      │
│      ├─ ...                                                 │
│      └─ Procesa fila 500                                    │
│                                                              │
│  Si cualquier fila falla → ROLLBACK total ⚠️                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 3: Procesar Cada Fila                                │
│  ───────────────────────────────────────────────────────    │
│  Para cada fila:                                            │
│      3.1 → Procesar Docente                                 │
│      3.2 → Procesar Comisión                                │
│      3.3 → Actualizar estadísticas                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  PASO 4: Resumen Final                                      │
│  ───────────────────────────────────────────────────────    │
│  📊 RESUMEN:                                                 │
│  👤 Docentes: 45 creados, 10 ya existían                    │
│  📚 Comisiones: 120 creadas, 5 actualizadas                 │
│  ✅ Sin errores                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Ejemplo de Archivo CSV

```csv
Período lectivo,Actividad,Comisión,Modalidad,Docente,Horario
PRIMER CUATRIMESTRE 2025,205 (PRI) - DERECHO ROMANO,0620,Presencial,GARCÍA JUAN,Lun 07:00 - 10:30
PRIMER CUATRIMESTRE 2025,2X8 (PRI) - DERECHO DE DAÑOS,0016,Presencial,LÓPEZ MARÍA,Mie 10:00 - 13:30
PRIMER CUATRIMESTRE 2025,205 (PRI) - DERECHO ROMANO,0621,Remota,GARCÍA JUAN,Mar 14:00 - 17:30
PRIMER CUATRIMESTRE 2025,339 (PRI) - CIVIL I,0010,Presencial,PÉREZ CARLOS,Jue 08:00 - 11:30
```

---

## 🔍 PASO 3.1: Procesamiento de Docente

### Entrada
```python
row = {
    'Docente': 'GARCÍA JUAN'
}
```

### Lógica Interna

```python
# 1. PARSEAR NOMBRE
docente_nombre_completo = 'GARCÍA JUAN'

# 2. SEPARAR APELLIDO Y NOMBRE
partes = ['GARCÍA', 'JUAN']
apellido = 'GARCÍA'     # Primera palabra
nombre = 'JUAN'         # Resto de palabras

# 3. BUSCAR DUPLICADO (get_or_create)
docente, created = Docente.objects.get_or_create(
    nombre_completo__iexact='GARCÍA JUAN',  # Búsqueda case-insensitive
    defaults={
        'nombre': 'Juan',           # .title() capitaliza
        'apellido': 'García',       # .title() capitaliza
        'nombre_completo': 'García Juan',
    }
)
```

### ¿Qué pasa con duplicados?

**Escenario 1: Primera vez**
```python
# El docente NO existe en la BD
created = True
# Se crea: García Juan ✅
```

**Escenario 2: Ya existe EXACTAMENTE**
```python
# BD ya tiene: 'García Juan'
# CSV tiene:   'GARCÍA JUAN'

# get_or_create con __iexact (case-insensitive):
created = False
# Reutiliza el existente ✅
# NO crea duplicado
```

**Escenario 3: Variaciones de nombre (PROBLEMA ⚠️)**
```python
# BD tiene:    'García Juan'
# CSV tiene:   'García Juan Carlos'

# get_or_create NO encuentra coincidencia
created = True
# Crea NUEVO docente 'García Juan Carlos' ❌
# → Ahora tienes 2 docentes similares
```

**Escenario 4: Orden diferente (PROBLEMA ⚠️)**
```python
# BD tiene:    'García Juan'
# CSV tiene:   'Juan García'

# get_or_create busca por nombre_completo exacto
created = True
# Crea NUEVO docente 'Juan García' ❌
```

---

## 🎯 PASO 3.2: Procesamiento de Comisión

### Entrada
```python
row = {
    'Actividad': '205 (PRI) - DERECHO ROMANO',
    'Comisión': '0620',
    'Horario': 'Lun 07:00 - 10:30',
    'Período lectivo': 'PRIMER CUATRIMESTRE ABOGACÍA 2025'
}
```

### Lógica Interna

```python
# 1. PARSEAR ACTIVIDAD con REGEX
actividad = '205 (PRI) - DERECHO ROMANO'

# Regex: r'^(\S+)\s+\([^)]+\)\s*-\s*(.+)$'
#        ^^^^        ^^^^       ^^^
#        205        (PRI)        -         DERECHO ROMANO
match = re.match(r'^(\S+)\s+\([^)]+\)\s*-\s*(.+)$', actividad)

if match:
    codigo_actividad = '205'                # Grupo 1
    nombre_actividad = 'DERECHO ROMANO'     # Grupo 2
else:
    # Si no tiene código, usar todo el nombre
    codigo_actividad = ''
    nombre_actividad = 'DERECHO ROMANO'

# 2. CREAR CÓDIGO ÚNICO
codigo_comision = '0620'
if codigo_actividad:
    codigo_unico = '205-0620'  # formato: {actividad}-{comision}
else:
    codigo_unico = '0620'       # solo comisión

# 3. EXTRAER CUATRIMESTRE
periodo = 'PRIMER CUATRIMESTRE ABOGACÍA 2025'
#         ^^^^^^                         ^^^^
cuatrimestre = '1C2025'  # formato: {1|2}{C|B}{año}

# 4. BUSCAR/CREAR COMISIÓN
comision, created = Comision.objects.update_or_create(
    codigo='205-0620',  # Busca por código único
    defaults={
        'nombre': 'DERECHO ROMANO',
        'docente': docente,  # Del paso anterior
        'horario': 'Lun 07:00 - 10:30',
        'cuatrimestre': '1C2025',
        'activa': True,
    }
)
```

### ¿Qué pasa con duplicados?

**Escenario 1: Comisión nueva**
```python
# El código '205-0620' NO existe
created = True
# Se crea la comisión ✅
```

**Escenario 2: Comisión ya existe (sin --update-existing)**
```python
# El código '205-0620' ya existe
# Modo por defecto: skip

if not update_existing and Comision.objects.filter(codigo=codigo_unico).exists():
    stats['comisiones_omitidas'] += 1
    return stats  # No hace nada ✅
```

**Escenario 3: Comisión ya existe (con --update-existing)**
```python
# El código '205-0620' ya existe
# Modo update_existing=True

comision, created = Comision.objects.update_or_create(
    codigo='205-0620',
    defaults={...}  # Actualiza todos los campos
)

created = False
# Actualiza: docente, horario, cuatrimestre ⚠️
```

---

## 🛡️ Manejo de Errores de Usuario

### Error 1: Fila sin docente
```python
# CSV:
# ,205 (PRI) - DERECHO ROMANO,0620,...

docente_nombre_completo = ''  # Campo vacío

if not docente_nombre_completo:
    return stats  # ⏭️ Omite la fila sin mensajes de error
```

**Resultado:** La fila se ignora silenciosamente.

---

### Error 2: Fila sin código de comisión
```python
# CSV:
# GARCÍA JUAN,DERECHO ROMANO,,Presencial,...

codigo_comision = ''  # Campo vacío

if not actividad or not codigo_comision:
    return stats  # ⏭️ Omite la fila
```

**Resultado:** La fila se ignora silenciosamente.

---

### Error 3: Nombre de docente con un solo término
```python
# CSV:
# GARCÍA,205 (PRI) - DERECHO ROMANO,0620,...

partes = ['GARCÍA']  # Solo 1 palabra
if len(partes) >= 2:
    # No entra aquí
else:
    apellido = 'GARCÍA'
    nombre = ''  # Nombre vacío

# Se crea: Docente(nombre='', apellido='García', nombre_completo='García')
```

**Resultado:** Funciona, pero con nombre vacío ⚠️

---

### Error 4: Actividad sin formato esperado
```python
# CSV: Actividad = "DERECHO ROMANO" (sin código)

match = re.match(r'^(\S+)\s+\([^)]+\)\s*-\s*(.+)$', 'DERECHO ROMANO')
# match = None

if match:
    # No entra
else:
    codigo_actividad = ''
    nombre_actividad = 'DERECHO ROMANO'

# Código final: solo el código de comisión
codigo_unico = '0620'  # Sin prefijo
```

**Resultado:** Funciona, pero sin código de actividad ✅

---

### Error 5: Encoding incorrecto (Excel guardado mal)
```python
# Si el CSV está en Latin-1 y se lee como UTF-8:

with open(file_path, 'r', encoding='utf-8') as f:
    # Falla al leer 'García' → UnicodeDecodeError ❌
```

**Resultado:** El comando falla completamente con error.

**Solución:** Siempre guardar CSV como UTF-8.

---

### Error 6: Delimitador incorrecto
```python
# CSV con ; pero esperamos ,
# "GARCÍA JUAN;205 (PRI) - DERECHO ROMANO;0620"

# SOLUCIÓN IMPLEMENTADA: Detección automática
sample = f.read(1024)
delimiter = ',' if sample.count(',') > sample.count(';') else ';'

# Usa el delimitador correcto ✅
```

**Resultado:** Se adapta automáticamente.

---

## ⚠️ Transacciones Atómicas: TODO O NADA

### ¿Qué es una transacción atómica?

```python
with transaction.atomic():
    # TODO dentro de este bloque es una transacción
    
    for row in data:  # 1000 filas
        process_row(row)  # Procesa cada fila
    
    if dry_run:
        transaction.set_rollback(True)  # Deshace TODO
```

### Ejemplo: Importar 1000 filas

**Caso 1: Todo bien**
```
Fila 1: ✅ Creado docente + comisión
Fila 2: ✅ Creado docente + comisión
...
Fila 1000: ✅ Creado docente + comisión

→ COMMIT: Se guardan las 1000 filas ✅
```

**Caso 2: Error en fila 999 (PROBLEMA)**
```
Fila 1: ✅ Creado docente + comisión
Fila 2: ✅ Creado docente + comisión
...
Fila 998: ✅ Creado docente + comisión
Fila 999: ❌ Error: código duplicado o formato inválido

→ ROLLBACK: Se pierden las 998 filas anteriores ❌
Usuario debe corregir fila 999 y volver a importar TODO
```

### ¿Por qué se usa transacción atómica?

**Ventaja:** Protege la integridad de datos
```
Sin transacción: Si falla a la mitad, quedas con datos a medias
Con transacción: O importas todo o no importas nada
```

**Desventaja:** Frustrante para archivos grandes
```
1 error = pierdes todo el progreso
```

---

## 🎛️ Modos de Operación

### Modo 1: Importación Normal
```bash
python manage.py import_comisiones archivo.csv
```

**Comportamiento:**
- Crea nuevos docentes
- Crea nuevas comisiones
- **Omite** comisiones que ya existen (por código)
- Guarda en la BD

**Salida:**
```
✅ 50 filas leídas

  👤 Docente creado: García Juan
  ✅ Comisión creada: 205-0620 - DERECHO ROMANO
  👤 Docente creado: López María
  ✅ Comisión creada: 2X8-0016 - DERECHO DE DAÑOS
  
📊 RESUMEN:
👤 Docentes: 2 creados, 0 ya existentes
📚 Comisiones: 2 creadas, 0 actualizadas, 0 omitidas
```

---

### Modo 2: Dry-Run (Simulación)
```bash
python manage.py import_comisiones archivo.csv --dry-run
```

**Comportamiento:**
- Procesa todo igual
- Muestra estadísticas
- **NO guarda nada** (rollback al final)
- Útil para verificar antes de importar

**Salida:**
```
🔍 Modo DRY-RUN: No se guardará nada en la base de datos

✅ 50 filas leídas

  👤 Docente creado: García Juan
  ✅ Comisión creada: 205-0620 - DERECHO ROMANO
  ...

📊 RESUMEN:
⚠️  Modo DRY-RUN (no se guardó nada)
👤 Docentes: 2 creados, 0 ya existentes
📚 Comisiones: 2 creadas, 0 actualizadas
```

**Uso recomendado:**
```bash
# 1. Primero verificar con dry-run
python manage.py import_comisiones archivo.csv --dry-run

# 2. Si todo se ve bien, importar de verdad
python manage.py import_comisiones archivo.csv
```

---

### Modo 3: Update Existing (Actualización)
```bash
python manage.py import_comisiones archivo.csv --update-existing
```

**Comportamiento:**
- Crea docentes nuevos
- **Actualiza** comisiones existentes (no omite)
- Útil para sincronizar cambios (docente cambió, horario cambió, etc.)

**Salida:**
```
✅ 50 filas leídas

  👤 Docente ya existe: García Juan
  📝 Comisión actualizada: 205-0620
  👤 Docente creado: López María
  ✅ Comisión creada: 2X8-0016 - DERECHO DE DAÑOS

📊 RESUMEN:
👤 Docentes: 1 creado, 1 ya existente
📚 Comisiones: 1 creada, 1 actualizada, 0 omitidas
```

**⚠️ CUIDADO:** Esto puede sobrescribir datos editados manualmente.

---

## 🔄 Comparación de Modos

| Situación | Normal | Dry-Run | Update-Existing |
|-----------|--------|---------|-----------------|
| Docente nuevo | Crea ✅ | Simula | Crea ✅ |
| Docente existente | Reutiliza ✅ | Simula | Reutiliza ✅ |
| Comisión nueva | Crea ✅ | Simula | Crea ✅ |
| Comisión existente | Omite ⏭️ | Simula | **Actualiza** 🔄 |
| Guarda en BD | Sí ✅ | **No** ❌ | Sí ✅ |

---

## 📊 Estadísticas Detalladas

### Contadores
```python
stats = {
    'docentes_creados': 0,        # Nuevos docentes
    'docentes_existentes': 0,     # Docentes reutilizados
    'comisiones_creadas': 0,      # Nuevas comisiones
    'comisiones_actualizadas': 0, # Comisiones modificadas
    'comisiones_omitidas': 0,     # Comisiones ignoradas
    'errores': 0,                 # Errores encontrados
}
```

### Ejemplo de salida completa
```
============================================================
📊 RESUMEN DE IMPORTACIÓN
============================================================

👤 Docentes:
   • Creados: 45
   • Ya existentes: 10

📚 Comisiones:
   • Creadas: 120
   • Actualizadas: 5
   • Omitidas: 15

✅ Sin errores

============================================================
```

---

## 🐛 Casos Problemáticos Reales

### Problema 1: Nombres compuestos
```csv
Docente: "Juan García Pérez"

# Parsing actual:
apellido = "Juan"           ❌
nombre = "García Pérez"     ❌

# Debería ser:
apellido = "García Pérez"   ✅
nombre = "Juan"              ✅
```

**Solución:** Usar columnas separadas:
```csv
Apellido,Nombre,Actividad,...
García Pérez,Juan,205 (PRI) - DERECHO ROMANO,...
```

---

### Problema 2: Mismo docente, nombres diferentes
```csv
Fila 1: GARCÍA JUAN
Fila 50: GARCIA JUAN         (sin acento)
Fila 100: García, Juan       (con coma)
Fila 150: J. García          (abreviado)
```

**Resultado actual:** Crea 4 docentes diferentes ❌

**Solución:** Normalizar en CSV antes de importar.

---

### Problema 3: Comisiones sin código de actividad
```csv
Actividad: "DERECHO ROMANO"  (sin "205 (PRI) -")
Comisión: "0620"

# Código generado: "0620"
```

**Riesgo:** Si hay otra materia con comisión "0620", genera conflicto.

**Solución:** Siempre incluir código de actividad.

---

### Problema 4: Transacción falla al final
```
Importando 5000 filas...
Fila 4999: Error - Código duplicado

→ Rollback: Se pierden 4998 filas procesadas
→ Usuario debe corregir CSV y empezar de nuevo
```

**Solución futura:** Implementar `--continue-on-error`

---

## 💡 Mejoras Sugeridas

### 1. Modo tolerante a errores
```bash
python manage.py import_comisiones archivo.csv --continue-on-error
```

**Lógica:**
```python
for row in data:
    try:
        process_row(row)
    except Exception as e:
        # Loguear error pero continuar
        stats['errores'] += 1
        error_log.append({'fila': i, 'error': str(e)})
        continue  # No rompe todo
```

---

### 2. Log de cambios
```bash
python manage.py import_comisiones archivo.csv --log-changes=cambios.json
```

**Output:**
```json
{
  "fecha": "2026-01-08 10:30:00",
  "docentes_creados": [
    {"id": 1, "nombre": "García Juan"},
    {"id": 2, "nombre": "López María"}
  ],
  "comisiones_actualizadas": [
    {
      "codigo": "205-0620",
      "cambios": {
        "docente": {"antes": "Pérez Carlos", "después": "García Juan"},
        "horario": {"antes": "Lun 10:00", "después": "Lun 07:00"}
      }
    }
  ]
}
```

---

### 3. Validación previa
```bash
python manage.py validate_csv archivo.csv
```

**Salida:**
```
🔍 Validando archivo...

⚠️  Fila 10: Docente vacío
⚠️  Fila 25: Código de comisión faltante
⚠️  Fila 50: Formato de actividad inválido
❌ Fila 100: Código duplicado '205-0620'

Total: 4 problemas encontrados
```

---

### 4. Preview de cambios
```bash
python manage.py import_comisiones archivo.csv --preview
```

**Salida:**
```
📊 PREVIEW DE IMPORTACIÓN (sin guardar):

Se crearán:
  • 45 docentes nuevos
  • 120 comisiones nuevas

Se actualizarán:
  • 5 comisiones existentes
    - 205-0620: Cambio de docente (Pérez → García)
    - 2X8-0016: Cambio de horario (10:00 → 14:00)
    - ...

Se omitirán:
  • 15 comisiones (ya existen, sin cambios)

¿Continuar? (s/n)
```

---

## 🎓 Resumen Ejecutivo

### ✅ Qué hace bien el sistema actual
- Maneja CSV y Excel
- Detecta delimitadores automáticamente
- Evita duplicados de docentes (case-insensitive)
- Evita duplicados de comisiones (por código único)
- Modo dry-run para testing
- Estadísticas detalladas
- Transacciones atómicas (integridad)

### ⚠️ Limitaciones actuales
- Parsing de nombres asume formato específico
- Transacción todo-o-nada (frustrante con archivos grandes)
- No maneja nombres con acentos de forma inteligente
- No hay log de cambios
- No hay validación previa
- Errores se ignoran silenciosamente (filas sin docente/código)

### 🚀 Flujo recomendado para usuarios
```bash
# 1. Verificar CSV primero
python manage.py import_comisiones archivo.csv --dry-run

# 2. Si todo OK, importar
python manage.py import_comisiones archivo.csv

# 3. Para actualizar datos existentes
python manage.py import_comisiones archivo.csv --update-existing --dry-run
python manage.py import_comisiones archivo.csv --update-existing
```

### 📝 Recomendaciones para el CSV
- Siempre UTF-8
- Formato: `APELLIDO NOMBRE` (sin comas ni guiones)
- Incluir código de actividad: `205 (PRI) - NOMBRE`
- Normalizar nombres (sin variaciones)
- No dejar campos vacíos
- Verificar códigos únicos
