# 📊 Sistema de Importación de Datos - Academic App

Sistema completo para importar docentes y comisiones desde archivos CSV o Excel.

---

## 📋 Tabla de Contenidos

1. [Formato de Archivo](#formato-de-archivo)
2. [Método 1: Command de Django](#método-1-command-de-django)
3. [Método 2: API REST](#método-2-api-rest)
4. [Ejemplos Prácticos](#ejemplos-prácticos)
5. [Solución de Problemas](#solución-de-problemas)

---

## 📄 Formato de Archivo

### Columnas Requeridas

| Columna | Descripción | Ejemplo | Requerido |
|---------|-------------|---------|-----------|
| **Período lectivo** | Período académico | `PRIMER CUATRIMESTRE ABOGACÍA 2025` | ✅ |
| **Actividad** | Código y nombre de materia | `205 (PRI) - DERECHO ROMANO` | ✅ |
| **Comisión** | Código de comisión | `0620` | ✅ |
| **Modalidad** | Presencial o Remota | `Presencial` | ✅ |
| **Docente** | Nombre completo | `LOCOCO JULIO` | ✅ |
| **Horario** | Días y horarios | `Lun 07:00 a 08:30 - Jue 07:00 a 08:30` | No |
| **RECOMENDACIÓN** | Texto libre | `Cátedra exigente...` | No |

### Formatos de Actividad Soportados

✅ **Con código:**
```
205 (PRI) - DERECHO ROMANO
2X8 (PRI) - DERECHO DE DAÑOS
```

✅ **Sin código:**
```
DERECHO ROMANO
TEORÍA GENERAL
```

El sistema detecta automáticamente el formato y extrae:
- **Código:** `205` (si existe)
- **Nombre:** `DERECHO ROMANO`

### Ejemplo de CSV

```csv
Período lectivo,Actividad,Comisión,Modalidad,Docente,Horario,RECOMENDACIÓN
PRIMER CUATRIMESTRE ABOGACÍA 2025,205 (PRI) - DERECHO ROMANO,0620,Presencial,LOCOCO JULIO,Lun 07:00 a 08:30 - Jue 07:00 a 08:30,Cátedra exigente
PRIMER CUATRIMESTRE ABOGACÍA 2025,2X8 (PRI) - DERECHO DE DAÑOS,0016,Presencial,COMPIANI MARIA F.,Lun 07:00 a 08:30 - Jue 07:00 a 08:30,Cátedra no recomendada
```

---

## 🔧 Método 1: Command de Django

### Instalación Previa (para Excel)

Si vas a importar archivos `.xlsx`:
```bash
pip install openpyxl
```

### Uso Básico

```bash
# Importar CSV
python manage.py import_comisiones ruta/al/archivo.csv

# Importar Excel
python manage.py import_comisiones ruta/al/archivo.xlsx
```

### Opciones Avanzadas

#### 1. **Modo DRY-RUN** (Simulación)
Simula la importación **sin guardar nada** en la base de datos:

```bash
python manage.py import_comisiones archivo.csv --dry-run
```

**Uso:** Perfecto para verificar que el archivo está bien formateado antes de importar.

#### 2. **Actualizar Existentes**
Actualiza comisiones que ya existen:

```bash
python manage.py import_comisiones archivo.csv --update-existing
```

**Comportamiento:**
- **Sin flag:** Omite comisiones que ya existen
- **Con flag:** Actualiza docente, horario, etc. de comisiones existentes

### Ejemplo Completo

```bash
# 1. Verificar primero en modo dry-run
python manage.py import_comisiones ~/Downloads/comisiones.csv --dry-run

# 2. Si todo está bien, importar de verdad
python manage.py import_comisiones ~/Downloads/comisiones.csv

# 3. Si necesitas actualizar datos existentes
python manage.py import_comisiones ~/Downloads/comisiones_actualizadas.csv --update-existing
```

### Salida del Command

```
📄 Leyendo CSV: /home/user/archivo.csv
✅ 100 filas leídas

  👤 Docente creado: Lococo Julio
  ✅ Comisión creada: 205-0620 - DERECHO ROMANO
  👤 Docente creado: Compiani Maria F.
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

---

## 🌐 Método 2: API REST

### Endpoint: Importar Archivo

```http
POST /api/docentes/import_file/
Content-Type: multipart/form-data
```

**Body (form-data):**
- `file`: archivo CSV o Excel
- `dry_run`: `true` o `false` (opcional, default: `false`)
- `update_existing`: `true` o `false` (opcional, default: `false`)

### Ejemplos con cURL

#### Importar CSV:
```bash
curl -X POST http://localhost:8000/api/docentes/import_file/ \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/ruta/al/archivo.csv"
```

#### Modo DRY-RUN:
```bash
curl -X POST http://localhost:8000/api/docentes/import_file/ \
  -F "file=@/ruta/al/archivo.csv" \
  -F "dry_run=true"
```

#### Con actualización:
```bash
curl -X POST http://localhost:8000/api/docentes/import_file/ \
  -F "file=@/ruta/al/archivo.csv" \
  -F "update_existing=true"
```

### Respuesta Exitosa

```json
{
  "success": true,
  "message": "Importación completada",
  "stats": {
    "docentes_creados": 10,
    "docentes_existentes": 5,
    "comisiones_creadas": 30,
    "comisiones_actualizadas": 0,
    "comisiones_omitidas": 2,
    "errores": 0
  },
  "output": "...detalle de la importación..."
}
```

### Respuesta con Error

```json
{
  "success": false,
  "error": "El archivo está mal formateado: falta la columna 'Docente'"
}
```

---

## 📚 Método 3: Bulk Create de Docentes

Para crear múltiples docentes **sin archivo CSV**:

```http
POST /api/docentes/bulk_create/
Content-Type: application/json
```

**Body:**
```json
{
  "docentes": [
    {"nombre": "Juan", "apellido": "García"},
    {"nombre": "María", "apellido": "López"},
    {"nombre": "Pedro", "apellido": "Martínez"}
  ]
}
```

**Respuesta:**
```json
{
  "success": true,
  "created_count": 3,
  "docentes": [
    {
      "id_docente": 1,
      "nombre": "Juan",
      "apellido": "García",
      "nombre_completo": "Juan García",
      "alias_search": ""
    },
    ...
  ]
}
```

---

## 💡 Ejemplos Prácticos

### Caso 1: Primera Importación

```bash
# Tienes un archivo CSV nuevo
python manage.py import_comisiones comisiones_1c2025.csv
```

**Resultado:**
- Crea todos los docentes nuevos
- Crea todas las comisiones

### Caso 2: Actualizar Datos

```bash
# Cambió el docente de algunas comisiones
python manage.py import_comisiones comisiones_actualizadas.csv --update-existing
```

**Resultado:**
- Actualiza las comisiones existentes con los nuevos docentes
- Crea las comisiones nuevas

### Caso 3: Verificar Antes de Importar

```bash
# No estás seguro del formato
python manage.py import_comisiones archivo_sospechoso.csv --dry-run
```

**Resultado:**
- Te muestra qué se importaría
- **NO guarda nada** en la base de datos
- Muestra errores si los hay

### Caso 4: Importar desde Web

```javascript
// Frontend (JavaScript)
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('dry_run', false);

fetch('/api/docentes/import_file/', {
  method: 'POST',
  body: formData,
})
  .then(response => response.json())
  .then(data => {
    console.log('Importación exitosa:', data.stats);
  });
```

---

## 🔍 Cómo Funciona Internamente

### 1. **Parsing de Docentes**

```
Input: "LOCOCO JULIO"
↓
Parsing:
- Apellido: "LOCOCO"
- Nombre: "JULIO"
- Nombre completo: "Lococo Julio" (title case)
↓
Busca en DB: ¿Existe "Lococo Julio"?
- ❌ No existe → CREA nuevo docente
- ✅ Existe → USA el existente
```

### 2. **Parsing de Actividad**

```
Caso A: Con código
Input: "205 (PRI) - DERECHO ROMANO"
↓
Extracción (regex):
- Código: "205"
- Nombre: "DERECHO ROMANO"
- Código final: "205-0620" (código + comisión)

Caso B: Sin código
Input: "DERECHO ROMANO"
↓
Extracción:
- Código: "" (vacío)
- Nombre: "DERECHO ROMANO"
- Código final: "0620" (solo comisión)
```

### 3. **Creación de Comisiones**

```
Busca comisión por código único
↓
¿Existe?
├─ ❌ No → CREA nueva comisión
└─ ✅ Sí
   ├─ ¿update_existing=true?
   │  ├─ ✅ Sí → ACTUALIZA comisión
   │  └─ ❌ No → OMITE (no hace nada)
```

---

## ❗ Solución de Problemas

### Problema 1: "No se encuentra la columna 'Docente'"

**Causa:** El CSV no tiene los nombres de columna correctos.

**Solución:**
Asegúrate de que la primera fila tenga estos nombres exactos:
```csv
Período lectivo,Actividad,Comisión,Modalidad,Docente,Horario,RECOMENDACIÓN
```

### Problema 2: "openpyxl not found"

**Causa:** Intentas importar un archivo Excel sin tener instalada la librería.

**Solución:**
```bash
pip install openpyxl
```

### Problema 3: Docentes duplicados

**Causa:** El mismo docente aparece con diferentes formatos:
- `GARCIA JUAN`
- `García Juan`
- `Garcia, Juan`

**Solución:** Normaliza los nombres en el CSV antes de importar, usando el formato:
```
APELLIDO NOMBRE
```

### Problema 4: Caracteres raros en nombres

**Causa:** Encoding incorrecto del CSV.

**Solución:** Guarda el CSV con encoding **UTF-8**:
- Excel: "Guardar como" → CSV UTF-8
- Google Sheets: "Descargar" → CSV

### Problema 5: Muchos errores al importar

**Usa dry-run primero:**
```bash
python manage.py import_comisiones archivo.csv --dry-run
```

Esto te mostrará **todos los errores** sin guardar nada.

---

## 📊 Validaciones Automáticas

El sistema valida automáticamente:

✅ **Códigos únicos:** No permite comisiones duplicadas  
✅ **Docentes duplicados:** Detecta docentes con el mismo nombre  
✅ **Campos requeridos:** Verifica que existan Actividad, Comisión, Docente  
✅ **Formatos:** Acepta múltiples formatos de actividad  
✅ **Longitud de campos:** Trunca nombres largos (máx 200 caracteres)

---

## 🎯 Mejores Prácticas

1. **Siempre usa dry-run primero:**
   ```bash
   python manage.py import_comisiones archivo.csv --dry-run
   ```

2. **Mantén el formato consistente:**
   - Usa siempre `APELLIDO NOMBRE` para docentes
   - Respeta los nombres de columnas exactos

3. **Haz backup antes de actualizar:**
   ```bash
   python manage.py dumpdata academic > backup_academic.json
   ```

4. **Importa por cuatrimestre:**
   - No mezcles datos de diferentes períodos en un solo archivo
   - Usa un archivo por cuatrimestre

5. **Verifica después de importar:**
   ```bash
   # Ver estadísticas
   curl http://localhost:8000/api/docentes/estadisticas/
   ```

---

## 🔗 Endpoints Relacionados

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/docentes/` | GET | Listar docentes |
| `/api/docentes/{id}/` | GET | Ver docente con comisiones |
| `/api/docentes/import_file/` | POST | Importar CSV/Excel |
| `/api/docentes/bulk_create/` | POST | Crear múltiples docentes |
| `/api/docentes/estadisticas/` | GET | Ver estadísticas |
| `/api/catedras/` | GET | Listar comisiones |
| `/api/catedras/{id}/` | GET | Ver comisión con docente |

---

## 📞 Soporte

¿Problemas? Revisa:
1. Este README
2. Los logs del servidor Django
3. La sección de "Solución de Problemas"

---

**Última actualización:** 8 de enero de 2026
