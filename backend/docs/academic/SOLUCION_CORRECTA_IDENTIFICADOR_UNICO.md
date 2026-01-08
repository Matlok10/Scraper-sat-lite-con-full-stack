# 🔧 Solución Correcta: Identificador Único Correcto

## El Problema Real Identificado

```
Tabla real del Excel:

Fila 5:  0620 - 205 (PRI) DERECHO ROMANO - LOCOCO JULIO - Lun 07:00 a 08:30
Fila 6:  0016 - 2X8 (PRI) DERECHO DAÑOS - COMPIANI MARIA - Lun 07:00 a 08:30
Fila 7:  0381 - 73U (PRI) DOMINIO FIDUCIARIO - ACEVEDO MARIA - Lun 07:00 a 08:30

← Todos tienen DIFERENTES comisiones (0620, 0016, 0381) ✅
```

## ¿Qué ES Realmente Duplicado?

**Caso 1: Duplicado EXACTO (error del usuario)**
```
Fila 20: 0027 - 2X8 (PRI) DERECHO DAÑOS - MARTINEZ G. - Lun 10:00 a 11:30
Fila 21: 0027 - 2X8 (PRI) DERECHO DAÑOS - MARTINEZ G. - Lun 10:00 a 11:30
         ↑                                           ↑
    MISMO TODO = Copypaste accidental
```

**Caso 2: MISMO horario pero diferente DOCENTE (error de datos)**
```
Fila 20: 0027 - 2X8 (PRI) DERECHO DAÑOS - MARTINEZ G. - Lun 10:00 a 11:30
Fila 21: 0027 - 2X8 (PRI) DERECHO DAÑOS - LENCINA M.  - Lun 10:00 a 11:30
         ↑                                      ↑ diferente
    ¿Una comisión no puede tener 2 docentes al mismo tiempo!
```

**Caso 3: MISMA comisión, DIFERENTE horario (VÁLIDO - múltiples horarios)**
```
Fila 20: 0027 - 2X8 (PRI) DERECHO DAÑOS - MARTINEZ G. - Lun 10:00 a 11:30
Fila 21: 0027 - 2X8 (PRI) DERECHO DAÑOS - MARTINEZ G. - Mar 14:00 a 15:30
         ↑                                                         ↑ diferente
    ✅ VÁLIDO - Misma comisión, misma materia, PERO en 2 horarios
    (estudiante puede elegir entre Lun o Mar)
```

---

## ✅ Solución: Identificador Único = Código Comisión + Horario + Docente + Período

```python
# El identificador único CORRECTO es la combinación de:
identificador_unico = f"{codigo_comision}|{docente_id}|{horario}|{cuatrimestre}"

# Ejemplos:
# "0027|1|Lun 10:00 a 11:30|1C2025" ← Válido
# "0027|1|Mar 14:00 a 15:30|1C2025" ← También válido (mismo código, diferente horario)
# "0027|2|Lun 10:00 a 11:30|1C2025" ← Error (misma comisión, diferente docente)
```

---

## 🔍 Detección de Problemas

### Tipo 1: Duplicado Exacto (IGNORAR)
```python
if registro_anterior == registro_actual:
    # Copypaste accidental
    # Omitir este registro
```

### Tipo 2: Mismo Código Comisión pero Diferente Docente (ERROR)
```python
comisiones_por_codigo = defaultdict(list)

for comision in data:
    codigo = comision['codigo_comision']
    comisiones_por_codigo[codigo].append(comision)

for codigo, instancias in comisiones_por_codigo.items():
    docentes = set(inst['docente_id'] for inst in instancias)
    if len(docentes) > 1:
        # ERROR: Una comisión no puede tener múltiples docentes
        raise ValueError(f"Comisión {codigo} asignada a {len(docentes)} docentes")
```

### Tipo 3: Mismo Código pero Diferente Horario (VÁLIDO)
```python
# Crear 2 registros diferentes:
# - Comisión 0027 | Docente: MARTINEZ | Horario: Lun 10:00
# - Comisión 0027 | Docente: MARTINEZ | Horario: Mar 14:00
# (pero con identificadores únicos diferentes internamente)
```

---

## 🗄️ Modelo de Datos Mejorado

### Opción A: Una tabla con identificador único compuesto

```python
class Comision(models.Model):
    # Campos originales
    codigo_comision = models.CharField(max_length=50)        # 0620, 0016, etc.
    codigo_actividad = models.CharField(max_length=50)       # 205, 2X8, 73U, 85S
    nombre_actividad = models.CharField(max_length=200)      # "DERECHO ROMANO"
    docente = models.ForeignKey(Docente, ...)
    horario = models.CharField(max_length=100)               # "Lun 07:00 a 08:30"
    cuatrimestre = models.CharField(max_length=10)           # "1C2025", "1B2025"
    modalidad = models.CharField(max_length=50)              # "Presencial", "Remota"
    
    class Meta:
        # Combinación de campos = identificador único
        unique_together = [
            ['codigo_comision', 'docente', 'horario', 'cuatrimestre']
        ]
    
    def __str__(self):
        return f"{self.codigo_comision}: {self.nombre_actividad} ({self.docente.apellido}) {self.horario}"
```

### Opción B: Tabla separada de Horarios (mejor para comisiones con múltiples horarios)

```python
class Comision(models.Model):
    codigo_comision = models.CharField(max_length=50, unique=True)
    codigo_actividad = models.CharField(max_length=50)
    nombre_actividad = models.CharField(max_length=200)
    docente = models.ForeignKey(Docente, ...)
    cuatrimestre = models.CharField(max_length=10)
    modalidad = models.CharField(max_length=50)

class HorarioComision(models.Model):
    comision = models.ForeignKey(Comision, related_name='horarios')
    horario = models.CharField(max_length=100)
    
    class Meta:
        unique_together = [['comision', 'horario']]
```

---

## 📋 Lógica de Importación Correcta

```python
def process_import(file_path):
    """
    Importar comisiones detectando:
    1. Duplicados exactos (ignorar)
    2. Errores de múltiples docentes (rechazar)
    3. Múltiples horarios válidos (crear múltiples registros)
    """
    
    data = read_csv(file_path)
    
    # 1. AGRUPAR POR CÓDIGO DE COMISIÓN
    comisiones_por_codigo = defaultdict(list)
    
    for idx, row in enumerate(data, 1):
        codigo = row.get('Comisión', '').strip()
        comisiones_por_codigo[codigo].append((idx, row))
    
    # 2. VALIDAR CADA GRUPO
    problemas = []
    registros_validos = []
    
    for codigo, instancias in comisiones_por_codigo.items():
        # Agrupar por docente
        docentes = defaultdict(list)
        for fila, row in instancias:
            docente = row.get('Docente', '').strip()
            docentes[docente].append((fila, row))
        
        # ¿Múltiples docentes para UNA comisión? = ERROR
        if len(docentes) > 1:
            problemas.append({
                'tipo': 'ERROR_MULTIPLE_DOCENTES',
                'codigo': codigo,
                'docentes': list(docentes.keys()),
                'filas': [f for f, _ in instancias]
            })
            continue  # No procesar
        
        # Por cada docente, procesar horarios
        for docente, filas_y_rows in docentes.items():
            # Detectar duplicados exactos
            vistos = set()
            para_procesar = []
            
            for fila, row in filas_y_rows:
                hash_row = hash((
                    row.get('Actividad', '').strip(),
                    row.get('Docente', '').strip(),
                    row.get('Horario', '').strip(),
                    row.get('Modalidad', '').strip(),
                ))
                
                if hash_row in vistos:
                    # Duplicado exacto
                    problemas.append({
                        'tipo': 'DUPLICADO_EXACTO',
                        'codigo': codigo,
                        'fila': fila,
                        'accion': 'IGNORADO'
                    })
                    continue
                
                vistos.add(hash_row)
                para_procesar.append((fila, row))
            
            # Ahora sí, procesar (pueden haber múltiples horarios)
            for fila, row in para_procesar:
                registros_validos.append((fila, row))
    
    # 3. REPORTAR PROBLEMAS
    print(f"\n⚠️  PROBLEMAS DETECTADOS:")
    for p in problemas:
        if p['tipo'] == 'ERROR_MULTIPLE_DOCENTES':
            print(f"  ❌ Comisión {p['codigo']} asignada a múltiples docentes:")
            for d in p['docentes']:
                print(f"     - {d}")
            print(f"     Filas: {p['filas']}")
        elif p['tipo'] == 'DUPLICADO_EXACTO':
            print(f"  ⚠️  Comisión {p['codigo']} (fila {p['fila']}) - Duplicado exacto - IGNORADO")
    
    # 4. PROCESAR REGISTROS VÁLIDOS
    print(f"\n✅ Procesando {len(registros_validos)} registros válidos...")
    for fila, row in registros_validos:
        procesar_row(row)
```

---

## 📊 Ejemplo de Salida Correcta

```bash
$ python manage.py import_comisiones archivo.xlsx

📄 Leyendo Excel: archivo.xlsx
✅ 100 filas leídas

🔍 Análisis de datos:

⚠️  PROBLEMAS DETECTADOS:

  ❌ Comisión 0027 asignada a múltiples docentes:
     - MARTINEZ GARBINO C.
     - LENCINA MARCELO
     Filas: 20, 21
     → NO se procesan estas filas

  ⚠️  Comisión 0016 (fila 50) - Duplicado exacto - IGNORADO

✅ Procesando 98 registros válidos...

  👤 Docente reutilizado: GARCÍA JUAN
  ✅ Comisión 0620 creada: 2X8 - DERECHO DAÑOS (COMPIANI) Lun 07:00-08:30
  ✅ Comisión 0027 creada: 2X8 - DERECHO DAÑOS (MARTINEZ) Lun 10:00-11:30
  ✅ Comisión 0027 creada: 2X8 - DERECHO DAÑOS (MARTINEZ) Mar 14:00-15:30
  
  ↑ NOTA: Misma comisión (0027), MISMA materia, MISMO docente
         PERO diferentes horarios = 2 registros diferentes ✅

============================================================
📊 RESUMEN DE IMPORTACIÓN
============================================================

👤 Docentes:
   • Creados: 25
   • Ya existentes: 15

📚 Comisiones:
   • Creadas: 98
   • Actualizadas: 0

⚠️  PROBLEMAS:
   • Duplicados exactos omitidos: 1
   • Errores de múltiples docentes: 1

✅ Sin más errores

============================================================
```

---

## 🎯 Cambios en el Comando

### Cambio 1: Validar múltiples docentes por comisión

```python
def validate_multiple_docentes(self, data):
    """
    Valida que una comisión no esté asignada a múltiples docentes
    en el MISMO período.
    """
    comisiones = defaultdict(set)
    
    for row in data:
        codigo = (row.get('Comisión') or '').strip()
        docente = (row.get('Docente') or '').strip()
        periodo = (row.get('Período lectivo') or '').strip()
        
        key = f"{codigo}|{periodo}"
        comisiones[key].add(docente)
    
    errores = []
    for key, docentes in comisiones.items():
        if len(docentes) > 1:
            codigo, periodo = key.split('|')
            errores.append(f"Comisión {codigo} ({periodo}): {len(docentes)} docentes diferentes")
    
    return errores
```

### Cambio 2: Permitir múltiples horarios

```python
# En lugar de usar solo código como único:
codigo_unico = codigo_comision

# Usar combinación que permita múltiples horarios:
identificador_unico = f"{codigo_comision}|{docente_id}|{horario}|{cuatrimestre}"

# O mejor: usar unique_together en el modelo
```

---

## 📝 Recomendación Final

**Usar la Opción A (único_together)** porque:
1. ✅ Simple de implementar
2. ✅ Permite múltiples horarios para misma comisión
3. ✅ Previene: múltiples docentes por comisión
4. ✅ Previene: duplicados exactos
5. ✅ Mantiene integridad de datos

**Modelo correcto:**

```python
class Comision(models.Model):
    codigo_comision = models.CharField(max_length=50)
    codigo_actividad = models.CharField(max_length=50)
    nombre_actividad = models.CharField(max_length=200)
    docente = models.ForeignKey(Docente, on_delete=models.SET_NULL, null=True)
    horario = models.CharField(max_length=100)
    cuatrimestre = models.CharField(max_length=10)
    modalidad = models.CharField(max_length=50)
    
    class Meta:
        # Identificador único: código + docente + horario + período
        unique_together = [
            ['codigo_comision', 'docente', 'horario', 'cuatrimestre']
        ]
        indexes = [
            models.Index(fields=['codigo_comision', 'cuatrimestre']),
            models.Index(fields=['docente', 'cuatrimestre']),
        ]
```

Así se permite:
- ✅ Mismo código (0027) con diferentes horarios
- ✅ Mismo código con mismo docente pero en períodos diferentes
- ❌ Mismo código + mismo docente + mismo horario + mismo período = Rechazado

