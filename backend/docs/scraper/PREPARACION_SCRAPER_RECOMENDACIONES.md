# 🎯 Preparación del Sistema para Scraper de Recomendaciones

**Fecha**: 8 de enero de 2026  
**Estado**: ✅ LISTO PARA SCRAPER  
**CSV Real**: 1751 comisiones importadas exitosamente

---

## 📊 Resumen de Cambios

Se ha preparado el sistema completo para absorber **TODAS las columnas del CSV** y dejar los campos listos para que el scraper procese las recomendaciones.

---

## 🗄️ Modelo `Comision` - Campos Agregados

### 1. **Campos que ya se llenan al importar**

```python
# Campo original (ya existía)
modalidad = CharField(
    choices=['Presencial', 'Remota', 'Híbrida']
)  # ✅ Se llena del CSV columna "Modalidad"

# Campo nuevo
recomendacion_raw = TextField()  
# ✅ Se llena del CSV columna "RECOMENDACIÓN" (texto completo sin procesar)
```

### 2. **Campos para el Scraper** (se llenan después)

Según el **instructivo de recomendaciones**, el scraper debe extraer:

```python
# 1️⃣ Probabilidad de aprobar (según instructivo punto 1)
tipo_catedra = CharField(
    choices=[
        ('recomendable', 'Cátedra Recomendable'),
        ('no_recomendable', 'Cátedra NO Recomendable'),
        ('exigente', 'Cátedra Exigente'),
        ('para_aprender', 'Cátedra para Aprender'),
        ('accesible', 'Cátedra Accesible'),
    ]
)

# 2️⃣ Info indispensable según instructivo punto 3
toma_asistencia = BooleanField()  # Punto 3.5: ¿Toma asistencia?
tipo_parciales = CharField()        # Punto 3.3: ¿Cómo son los parciales?
toma_trabajos_practicos = BooleanField()  # Punto 3.4: ¿Toma TPs?

# 3️⃣ Nivel de aprobados (según instructivo punto 2)
nivel_aprobados = CharField(
    choices=[
        ('alto', 'Alta tasa de aprobados'),      # "Buen nivel de aprobados"
        ('medio', 'Tasa media de aprobados'),
        ('bajo', 'Baja tasa de aprobados'),      # "No aprueba nadie"
    ]
)

# 4️⃣ Llegada del docente (según instructivo punto 3.2)
llegada_docente = CharField(
    choices=[
        ('buena', 'Buena llegada a los estudiantes'),  # "Los profesores son unos genios"
        ('mala', 'Mala llegada a los estudiantes'),    # "Tiene mala llegada"
        ('regular', 'Llegada regular'),
    ]
)

# 5️⃣ Bibliografía (según instructivo punto 3.6)
bibliografia_info = TextField()  # "la sube al campus", "hay que comprarla", etc.

# 6️⃣ Control de procesamiento
recomendacion_procesada = BooleanField(default=False)
# ✅ El scraper marca TRUE cuando termina de procesar
```

---

## 📋 Instructivo de Recomendaciones (para referencia del Scraper)

### ✅ ¿Qué va SI O SI en la reco?

#### 1️⃣ Probabilidad de aprobar (elegir solo una):
- **"Cátedra recomendable"** → Si estudias, vas a aprobar
- **"Cátedra NO recomendable"** → No hay que anotarse
- **"Cátedra exigente"** → Aunque estudies, puede que no apruebes

#### 2️⃣ Info importante para la cursada:
- No aprueba nadie (es una masacre)
- Clases densas (profes infumables)
- Tiene mala llegada a los estudiantes
- Toma todo el programa
- **Buen nivel de aprobados** (aprueban todos o casi todos)
- Los profesores son unos genios / explican muy bien
- Malas referencias entre los estudiantes
- Cátedra tranquila
- **Opiniones encontradas** entre los estudiantes
- Toma solo lo que da en clase

#### 3️⃣ Info **INDISPENSABLE**:
1. **¿Cómo viene la cátedra?** (recomendable/NO recomendable/exigente)
2. **¿Cómo es el docente?** (buena/mala llegada)
3. **¿Cómo son los parciales?** (escritos/orales/MC)
4. **Trabajos Prácticos** (Toma TPs / No toma TPs)
5. **Asistencia** (Toma asistencia / No toma asistencia)
6. **Bibliografía** (¿Qué usa? ¿La sube al campus? ¿Hay que comprarla?)
7. **Modalidad de cursada** (Ya viene en CSV: Presencial/Remota/Híbrida)

### ❌ ¿Qué NO va en la reco?
- Malos tratos → usar "mala llegada a los estudiantes"
- "X" (ej: profesorxs)
- Si acepta/No acepta oyentes
- Comentarios en lunfardo
- Copy-paste de comentarios

---

## 🔍 Ejemplos de Texto Real a Procesar

### Ejemplo 1:
**recomendacion_raw**:
```
Cátedra exigente. Toma el recuperatorio el mismo dia que el final. 
Son dos exámenes escritos, el primero es a desarrollar y el segundo 
es un poco más complejo.
```

**Scraper debe extraer**:
```python
tipo_catedra = 'exigente'
tipo_parciales = 'Dos parciales escritos a desarrollar'
toma_asistencia = None  # No menciona
toma_trabajos_practicos = False  # No menciona TPs
```

### Ejemplo 2:
**recomendacion_raw**:
```
Cátedra recomendable. Los profes tienen siempre buena predisposición, 
evalua con un trabajo practico grupal y un parcial a desarrollar. 
No toma asitencia y buena tasa de aprobados con notas altas.
```

**Scraper debe extraer**:
```python
tipo_catedra = 'recomendable'
llegada_docente = 'buena'  # "buena predisposición"
tipo_parciales = 'Parcial escrito a desarrollar'
toma_trabajos_practicos = True  # "trabajo practico grupal"
toma_asistencia = False  # "No toma asistencia"
nivel_aprobados = 'alto'  # "buena tasa de aprobados"
```

### Ejemplo 3:
**recomendacion_raw**:
```
Opiniones encontradas entre los estudiantes. Clases desorganizadas.
```

**Scraper debe extraer**:
```python
tipo_catedra = None  # No especifica claramente
llegada_docente = 'regular'  # "Opiniones encontradas"
# Otros campos: dejar en NULL
```

---

## 📂 Estructura del CSV Real

```
Columnas del CSV "MADRE CPO 1C2026.xlsx - Table 1.csv":
┌─────────────────────┬──────────────────────────────────────────────────┐
│ Columna             │ Descripción                                      │
├─────────────────────┼──────────────────────────────────────────────────┤
│ Período lectivo     │ Ej: "PRIMER CUATRIMESTRE ABOGACÍA 2025"         │
│ Actividad           │ Ej: "205 (PRI) ‐ DERECHO ROMANO"                │
│ Comisión            │ Ej: "0620"                                       │
│ Modalidad           │ Ej: "Presencial", "Remota"                       │
│ Docente             │ Ej: "LOCOCO JULIO"                               │
│ Horario             │ Ej: "Lun 07:00 a 08:30 ‐ Jue 07:00 a 08:30"    │
│ RECOMENDACIÓN       │ Texto largo con opinión (requiere procesamiento) │
└─────────────────────┴──────────────────────────────────────────────────┘

Total de registros: 1751 comisiones
Encoding: UTF-8-SIG
```

---

## ✅ Estado Actual del Sistema

### Migración 0005 Aplicada

```
✅ comision.modalidad (CharField con choices)
✅ comision.recomendacion_raw (TextField - texto original)
✅ comision.tipo_catedra (CharField con choices)
✅ comision.toma_asistencia (BooleanField)
✅ comision.tipo_parciales (CharField)
✅ comision.toma_trabajos_practicos (BooleanField)
✅ comision.nivel_aprobados (CharField con choices)
✅ comision.llegada_docente (CharField con choices)
✅ comision.bibliografia_info (TextField)
✅ comision.recomendacion_procesada (BooleanField, default=False)
```

### Comando de Importación Actualizado

```bash
# Importa el CSV real con todas las columnas
python manage.py import_comisiones "MADRE CPO 1C2026.xlsx - Table 1.csv"

✅ Lee 1751 comisiones
✅ Detecta duplicados automáticamente
✅ Guarda modalidad (Presencial/Remota)
✅ Guarda recomendacion_raw (texto completo)
✅ Permite múltiples horarios por comisión
✅ Maneja encoding UTF-8-SIG
✅ Salta headers automáticamente (líneas 1-3)
```

---

## 🤖 Flujo de Trabajo para el Scraper

### Paso 1: Importar CSV
```bash
cd backend
python manage.py import_comisiones "archivo.csv"
```
**Resultado**: 
- Todas las comisiones en DB
- `recomendacion_raw` lleno con texto original
- `recomendacion_procesada = False`

### Paso 2: Scraper procesa recomendaciones
```python
# Pseudo-código del scraper
from academic.models import Comision

# Obtener comisiones sin procesar
comisiones = Comision.objects.filter(recomendacion_procesada=False)

for comision in comisiones:
    texto = comision.recomendacion_raw
    
    # ANALIZAR TEXTO
    if "cátedra recomendable" in texto.lower():
        comision.tipo_catedra = 'recomendable'
    elif "cátedra no recomendable" in texto.lower():
        comision.tipo_catedra = 'no_recomendable'
    elif "cátedra exigente" in texto.lower():
        comision.tipo_catedra = 'exigente'
    
    if "no toma asistencia" in texto.lower():
        comision.toma_asistencia = False
    elif "toma asistencia" in texto.lower():
        comision.toma_asistencia = True
    
    if "trabajo practico" in texto.lower() or "tp" in texto.lower():
        comision.toma_trabajos_practicos = True
    
    # ... etc (extraer todos los campos)
    
    # Marcar como procesada
    comision.recomendacion_procesada = True
    comision.save()
```

### Paso 3: Verificar procesamiento
```bash
# Ver cuántas faltan procesar
python manage.py shell
>>> from academic.models import Comision
>>> Comision.objects.filter(recomendacion_procesada=False).count()
```

---

## 🎯 Próximos Pasos

### Para el desarrollador del Scraper:

1. **Crear comando Django**: `process_recomendaciones.py`
   ```bash
   python manage.py process_recomendaciones
   ```

2. **Usar NLP o regex** para extraer:
   - Tipo de cátedra (keywords: "recomendable", "exigente", "no recomendable")
   - Toma asistencia (keywords: "toma asistencia", "no toma asistencia")
   - Trabajos prácticos (keywords: "tp", "trabajo practico", "trabajos practicos")
   - Tipo de parciales (keywords: "parcial escrito", "oral", "multiple choice", "MC")
   - Nivel de aprobados (keywords: "alta tasa", "baja tasa", "aprueba nadie")
   - Llegada docente (keywords: "buena llegada", "mala llegada", "profesores genios")

3. **Manejar casos edge**:
   - "Opiniones encontradas" → llegada_docente = 'regular'
   - Sin información → dejar NULL
   - Texto ambiguo → dejar NULL o usar valor por defecto

4. **Logging**:
   - Guardar log de qué comisiones se procesaron
   - Reportar cuántos campos se llenaron vs cuántos quedaron NULL
   - Identificar textos que no se pudieron parsear

---

## 📊 Ejemplo de Resultado Final

```python
# Después de importar + scraper
comision = Comision.objects.get(codigo='0620')

print(f"Código: {comision.codigo}")
print(f"Nombre: {comision.nombre}")
print(f"Docente: {comision.docente.nombre_completo}")
print(f"Modalidad: {comision.modalidad}")
print(f"Horario: {comision.horario}")
print(f"\n--- RECOMENDACIÓN ORIGINAL ---")
print(f"{comision.recomendacion_raw}")
print(f"\n--- DATOS EXTRAÍDOS POR SCRAPER ---")
print(f"Tipo: {comision.tipo_catedra}")
print(f"Toma asistencia: {comision.toma_asistencia}")
print(f"Tipo parciales: {comision.tipo_parciales}")
print(f"Toma TPs: {comision.toma_trabajos_practicos}")
print(f"Nivel aprobados: {comision.nivel_aprobados}")
print(f"Llegada docente: {comision.llegada_docente}")
print(f"Procesada: {comision.recomendacion_procesada}")
```

**Output esperado**:
```
Código: 0620
Nombre: DERECHO ROMANO
Docente: Lococo Julio
Modalidad: Presencial
Horario: Lun 07:00 a 08:30 ‐ Jue 07:00 a 08:30

--- RECOMENDACIÓN ORIGINAL ---
Cátedra exigente. Toma el recuperatorio el mismo dia que el final. 
Son dos exámenes escritos, el primero es a desarrollar y el segundo 
es un poco más complejo.

--- DATOS EXTRAÍDOS POR SCRAPER ---
Tipo: exigente
Toma asistencia: None
Tipo parciales: Dos parciales escritos a desarrollar
Toma TPs: False
Nivel aprobados: None
Llegada docente: None
Procesada: True
```

---

## 🔧 Comandos Útiles

### Importar CSV real:
```bash
cd backend
python manage.py import_comisiones "/ruta/MADRE CPO 1C2026.xlsx - Table 1.csv"
```

### Ver estadísticas:
```python
from academic.models import Comision

# Total de comisiones
print(f"Total: {Comision.objects.count()}")

# Con recomendación
print(f"Con recomendación: {Comision.objects.exclude(recomendacion_raw__isnull=True).count()}")

# Procesadas
print(f"Procesadas: {Comision.objects.filter(recomendacion_procesada=True).count()}")

# Pendientes de procesar
print(f"Pendientes: {Comision.objects.filter(recomendacion_procesada=False, recomendacion_raw__isnull=False).count()}")
```

### Buscar keywords en recomendaciones:
```python
# Buscar "exigente"
Comision.objects.filter(recomendacion_raw__icontains='exigente').count()

# Buscar "no toma asistencia"
Comision.objects.filter(recomendacion_raw__icontains='no toma asistencia').count()
```

---

**Estado**: ✅ **SISTEMA LISTO PARA SCRAPER**  
**Próximo paso**: Desarrollar el comando `process_recomendaciones.py`
