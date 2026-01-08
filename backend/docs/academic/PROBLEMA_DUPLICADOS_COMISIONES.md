# 🔍 Problema Real: Duplicados y Variaciones en Importación

## El Escenario Actual

```csv
Período lectivo,Actividad,Comisión,Modalidad,Docente,Horario,RECOMENDACIÓN
PRIMER CUATRIMESTRE ABOGACÍA 2025,2X8 (PRI) ‐ DERECHO DE DAÑOS,0016,Presencial,COMPIANI MARIA F.,Lun 07:00 a 08:30 ‐ Jue 07:00 a 08:30,...
PRIMER CUATRIMESTRE ABOGACÍA 2025,2X8 (PRI) ‐ DERECHO DE DAÑOS,0277,Presencial,LENCINA MARCELO,Lun 08:30 a 10:00 ‐ Jue 08:30 a 10:00,...
PRIMER CUATRIMESTRE ABOGACÍA 2025,2X8 (PRI) ‐ DERECHO DE DAÑOS,0027,Presencial,MARTINEZ GARBINO C.,Lun 10:00 a 11:30 ‐ Jue 10:00 a 11:30,...
```

**¿Qué son estos números?**
- `0016`, `0277`, `0027` = Códigos únicos de COMISIÓN (no son actividades)
- Todos son la MISMA materia: "2X8 - DERECHO DE DAÑOS"
- Pero con DIFERENTES:
  - Docentes
  - Horarios
  - Grupos de estudiantes

---

## 🚨 El Problema Actual del Sistema

```python
# Código actual en import_comisiones.py
if codigo_actividad:
    codigo_unico = f"{codigo_actividad}-{codigo_comision}"  # Ejemplo: "2X8-0016"
else:
    codigo_unico = codigo_comision  # Ejemplo: "0016"
```

**Problema:**
```
CSV tiene:
Fila 1: Actividad="2X8...", Comisión="0016", Docente="COMPIANI MARIA F.", Horario="Lun 07:00"
Fila 2: Actividad="2X8...", Comisión="0016", Docente="COMPIANI MARIA F.", Horario="Lun 07:00"  ← DUPLICADO EXACTO
Fila 3: Actividad="2X8...", Comisión="0016", Docente="COMPIANI MARIA F.", Horario="Mar 14:00"  ← MISMO pero diferente horario

# Con el código actual:
codigo_unico = "2X8-0016"  # Todas generan el mismo código

# En importación:
Fila 1: Crea comisión "2X8-0016" ✅
Fila 2: Intenta crear "2X8-0016" → Ya existe → Omite o Actualiza ⚠️
Fila 3: Intenta crear "2X8-0016" → Ya existe → Sobrescribe el horario anterior ❌
        Ahora todas las comisiones 0016 tienen el mismo horario (Mar 14:00)
```

---

## ✅ La Solución Correcta

El código de comisión **SÍ es único** → **Usar solo el número de comisión como identificador**

```python
# SOLUCIÓN:
# El código de comisión (0016, 0277, 0027) YA es único
# No necesitamos agregar el código de actividad

codigo_unico = codigo_comision  # Solo: "0016", no "2X8-0016"

# En la BD:
Comision(
    codigo=0016,  # Identificador único ✅
    nombre="DERECHO DE DAÑOS",  # Nombre de la materia
    docente=COMPIANI_MARIA_F,
    horario="Lun 07:00 a 08:30",
    actividad_codigo="2X8",  # Opcional: guardar código de actividad
    ...
)
```

---

## 🎯 Detectar y Manejar Duplicados en el Archivo

```python
def process_import(file_path):
    """Procesar importación detectando duplicados."""
    
    data = read_csv(file_path)
    
    # 1. DETECTAR DUPLICADOS DENTRO DEL ARCHIVO
    duplicados_archivo = defaultdict(list)
    
    for idx, row in enumerate(data, 1):
        codigo_comision = row.get('Comisión', '').strip()
        if codigo_comision:
            duplicados_archivo[codigo_comision].append({
                'fila': idx,
                'docente': row.get('Docente'),
                'horario': row.get('Horario'),
                'hash': hash_row(row)  # Comparar contenido
            })
    
    # 2. ANALIZAR DUPLICADOS
    for codigo, apariciones in duplicados_archivo.items():
        if len(apariciones) > 1:
            # Hay duplicados para este código
            
            # ¿Son exactamente iguales?
            hashes = [a['hash'] for a in apariciones]
            if len(set(hashes)) == 1:
                # ❌ DUPLICADO EXACTO
                print(f"⚠️  Comisión {codigo} aparece {len(apariciones)} veces (idénticas)")
                print(f"    Filas: {[a['fila'] for a in apariciones]}")
                print(f"    Acción: Se procesará solo la primera")
            else:
                # ⚠️ MISMA COMISIÓN PERO DIFERENTE CONTENIDO
                print(f"⚠️  Comisión {codigo} aparece con variaciones:")
                for a in apariciones:
                    print(f"    Fila {a['fila']}: {a['docente']} - {a['horario']}")
                print(f"    Acción: Revisar archivo - posible error de datos")
    
    # 3. PROCESAR CON DEDUPLICACIÓN
    procesados = set()
    
    for row in data:
        codigo = row.get('Comisión', '').strip()
        
        if codigo in procesados:
            # Ya procesamos este código en este archivo
            stats['duplicados_omitidos'] += 1
            continue
        
        procesados.add(codigo)
        process_row(row)
```

---

## 📊 Ejemplo de Salida Mejorada

```bash
$ python manage.py import_comisiones archivo.csv

📄 Leyendo CSV: archivo.csv
✅ 100 filas leídas

🔍 Análisis de duplicados:
   ⚠️  Comisión 0016 aparece 2 veces (filas 1, 50) - IDÉNTICAS
   ⚠️  Comisión 0277 aparece 3 veces (filas 2, 51, 75) - CON VARIACIONES
       • Fila 2: LENCINA MARCELO - Lun 08:30
       • Fila 51: LENCINA MARCELO - Lun 08:30
       • Fila 75: MARTINEZ GARBINO - Mar 14:00
   ✅ Comisión 0027 - SIN DUPLICADOS

============================================================
📊 RESUMEN DE IMPORTACIÓN
============================================================

🔍 Análisis de Datos:
   • Filas leídas: 100
   • Comisiones únicas: 98
   • Duplicados exactos: 1
   • Variaciones detectadas: 2

⚠️  ADVERTENCIAS:
   • Comisión 0016 (filas 1, 50): Duplicado exacto - procesando solo primera
   • Comisión 0277 (filas 2, 51, 75): Verificar datos - aparece con variaciones

👤 Docentes:
   • Creados: 25
   • Ya existentes: 15

📚 Comisiones:
   • Creadas: 98
   • Actualizadas: 0
   • Omitidas (duplicados): 2

✅ Importación completada
   ⚠️  Revisa las ADVERTENCIAS arriba

============================================================
```

---

## 🔧 Cambios Necesarios en el Código

### 1. Cambiar generación de código único

**Antes:**
```python
if codigo_actividad:
    codigo_unico = f"{codigo_actividad}-{codigo_comision}"
else:
    codigo_unico = codigo_comision
```

**Después:**
```python
# El código de comisión YA es único en la realidad
codigo_unico = codigo_comision

# Pero guardamos el código de actividad por si lo necesitamos
# para búsquedas o reportes
codigo_actividad_guardado = codigo_actividad  # Para análisis
```

### 2. Agregar detección de duplicados en el archivo

```python
def detect_duplicates_in_file(data):
    """
    Detecta y reporta duplicados dentro del mismo archivo.
    
    Retorna:
        - Duplicados exactos (mismo contenido)
        - Variaciones (mismo código, diferente contenido)
    """
    duplicados_exactos = defaultdict(list)
    duplicados_variaciones = defaultdict(list)
    
    for idx, row in enumerate(data, 1):
        codigo = row.get('Comisión', '').strip()
        if not codigo:
            continue
        
        # Hash para comparar contenido
        content_hash = hash((
            row.get('Actividad', '').strip(),
            row.get('Docente', '').strip(),
            row.get('Horario', '').strip(),
        ))
        
        duplicados_exactos[codigo].append((idx, content_hash))
    
    # Analizar
    resultado = {
        'exactos': {},
        'variaciones': {},
        'warnings': []
    }
    
    for codigo, instancias in duplicados_exactos.items():
        if len(instancias) > 1:
            hashes = [h for _, h in instancias]
            if len(set(hashes)) == 1:
                # Duplicado exacto
                resultado['exactos'][codigo] = [i for i, _ in instancias]
                resultado['warnings'].append(
                    f"⚠️  Comisión {codigo} aparece {len(instancias)} veces (idénticas)"
                )
            else:
                # Variaciones
                resultado['variaciones'][codigo] = [i for i, _ in instancias]
                resultado['warnings'].append(
                    f"⚠️  Comisión {codigo} aparece con {len(set(hashes))} variaciones diferentes"
                )
    
    return resultado
```

### 3. Procesar sin duplicados

```python
def process_import_deduped(data):
    """Procesa pero omite duplicados del mismo archivo."""
    
    stats = {
        'procesadas': 0,
        'duplicados_exactos_omitidos': 0,
        'variaciones_advertidas': 0,
    }
    
    # Detectar duplicados primero
    dup_info = detect_duplicates_in_file(data)
    
    # Mostrar warnings
    for warning in dup_info['warnings']:
        print(warning)
    
    # Procesar solo primeras instancias
    procesados = set()
    
    for row in data:
        codigo = row.get('Comisión', '').strip()
        
        if codigo in procesados:
            # Ya procesamos este código
            if codigo in dup_info['exactos']:
                stats['duplicados_exactos_omitidos'] += 1
            elif codigo in dup_info['variaciones']:
                stats['variaciones_advertidas'] += 1
            continue
        
        procesados.add(codigo)
        process_row(row)
        stats['procesadas'] += 1
    
    return stats
```

---

## 📋 Modelo de Datos Propuesto

### Actual
```python
class Comision(models.Model):
    codigo = models.CharField(max_length=100, unique=True)  # "205-0620"
    nombre = models.CharField(max_length=200)               # "DERECHO ROMANO"
    docente = models.ForeignKey(Docente, ...)
    horario = models.CharField(max_length=200)
```

### Propuesto (MEJOR)
```python
class Comision(models.Model):
    codigo = models.CharField(max_length=50, unique=True)   # "0620" (único)
    nombre = models.CharField(max_length=200)               # "DERECHO ROMANO"
    codigo_actividad = models.CharField(max_length=50, blank=True)  # "205", "2X8"
    docente = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True)
    horario = models.CharField(max_length=200)
    modalidad = models.CharField(max_length=50)
    cuatrimestre = models.CharField(max_length=10)
    
    class Meta:
        unique_together = [['codigo']]  # Código de comisión es único
    
    def __str__(self):
        actividad = f"{self.codigo_actividad} - " if self.codigo_actividad else ""
        docente = f"({self.docente.apellido})" if self.docente else "(Sin docente)"
        return f"{self.codigo}: {actividad}{self.nombre} {docente}"
```

---

## 🎯 Flujo de Importación Mejorado

```
1. LEER ARCHIVO
   ↓
2. DETECTAR DUPLICADOS
   ├─ Duplicados exactos
   └─ Variaciones
   ↓
3. MOSTRAR WARNINGS
   "Comisión 0016 aparece 2 veces (idénticas)"
   "Comisión 0277 aparece con variaciones"
   ↓
4. PREGUNTAR AL USUARIO (en modo interactivo)
   "¿Continuar omitiendo duplicados? (s/n)"
   ↓
5. PROCESAR DEDUPLICANDO
   • Solo primera instancia de cada comisión
   • Advertencias sobre variaciones
   ↓
6. REPORTAR
   "98 comisiones únicas importadas"
   "2 duplicados exactos omitidos"
   "1 variación detectada - revisar fila 75"
```

---

## 💡 Casos de Uso

### Caso 1: Duplicado Exacto (Error del Usuario)
```csv
Fila 1: Comisión 0016 - DERECHO DAÑOS - COMPIANI - Lun 07:00
Fila 2: Comisión 0016 - DERECHO DAÑOS - COMPIANI - Lun 07:00
```

**Acción:** Omitir Fila 2, procesadera solo Fila 1 ✅

### Caso 2: Misma Comisión, Diferente Horario (Datos Conflictivos)
```csv
Fila 1: Comisión 0016 - DERECHO DAÑOS - COMPIANI - Lun 07:00
Fila 2: Comisión 0016 - DERECHO DAÑOS - COMPIANI - Mar 14:00
```

**Acción:** 
- Advertencia: "Variación detectada"
- Procesar Fila 1 (primera)
- Avisar al usuario: "Revisar Fila 2"

### Caso 3: Misma Comisión, Diferente Docente (Error Grave)
```csv
Fila 1: Comisión 0016 - DERECHO DAÑOS - COMPIANI
Fila 2: Comisión 0016 - DERECHO DAÑOS - LENCINA
```

**Acción:**
- Error: "Comisión 0016 asignada a dos docentes diferentes"
- No procesar
- Pedir corrección

---

## ✅ Resumen de la Solución

| Problema | Solución | Código |
|----------|----------|--------|
| Código no es único | Usar solo número de comisión | `codigo = "0016"` |
| Duplicados exactos | Detectar y omitir | `detect_duplicates_in_file()` |
| Variaciones | Advertir al usuario | `warnings.append()` |
| Sobrescrituras | Procesar solo primera | `if codigo in procesados: continue` |
| Falta claridad | Mejor reporte | Output con advertencias |
