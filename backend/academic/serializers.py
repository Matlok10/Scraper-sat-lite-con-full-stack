"""
Serializers para la app academic.

Contiene serializers anidados que permiten una representación jerárquica
de los datos académicos con validación y relaciones documentadas.
"""
from rest_framework import serializers
from .models import Docente, Comision


# ============================================================================
# SERIALIZERS BÁSICOS (Sin relaciones anidadas)
# ============================================================================

class DocenteSerializer(serializers.ModelSerializer):
    """
    Serializer básico para Docente.
    
    Usado para crear/actualizar docentes sin sus comisiones relacionadas.
    
    Campos:
        - id_docente: ID único del docente (read-only)
        - nombre: Nombre del docente
        - apellido: Apellido del docente
        - nombre_completo: Nombre completo (generado automáticamente)
        - alias_search: Aliases para búsqueda (separados por espacios/comas)
    """
    
    class Meta:
        model = Docente
        fields = ['id_docente', 'nombre', 'apellido', 'nombre_completo', 'alias_search']
        read_only_fields = ['id_docente', 'nombre_completo']


class ComisionSerializer(serializers.ModelSerializer):
    """
    Serializer básico para Comisión.
    
    Muestra solo el ID del docente (útil para escritura).
    
    Campos principales:
        - id_comision: ID único (read-only)
        - codigo: Código único de la comisión
        - nombre: Nombre de la comisión
        - docente: ID del docente asignado
        - horario: Horario de la comisión
        - etc.
    """
    class Meta:
        model = Comision
        fields = [
            'id_comision', 'codigo', 'nombre', 'docente', 'numero_catedra',
            'horario', 'cuatrimestre', 'modalidad', 'sede', 'es_centro_externo', 'ciclo',
            'mencion_fb', 'ano', 'activa',
            'ultima_actualizacion_scraping', 'fecha_creacion'
        ]
        read_only_fields = ['id_comision', 'fecha_creacion', 'ultima_actualizacion_scraping']


# ============================================================================
# SERIALIZERS ANIDADOS (Con relaciones incluidas)
# ============================================================================

class DocenteConComisionesSerializer(serializers.ModelSerializer):
    """
    Serializer ANIDADO para Docente que incluye sus comisiones.
    
    Cuando obtienes un docente con este serializer, recibirás:
    - Todos los datos del docente
    - Un array 'comisiones' con TODAS sus comisiones asociadas
    
    Útil para:
        - GET /api/docentes/{id}/ → Ver un docente + todas sus comisiones
        - Cuando necesitas la información completa de un docente
    
    Ejemplo de respuesta JSON:
    {
        "id_docente": 1,
        "nombre": "Juan",
        "apellido": "García",
        "nombre_completo": "Juan García",
        "alias_search": "J. García, Garcia, Juan G",
        "comisiones": [
            {
                "id_comision": 10,
                "codigo": "PROG1-A",
                "nombre": "Programación 1",
                "horario": "Lunes-Miércoles 10:00",
                ...
            },
            {
                "id_comision": 11,
                "codigo": "PROG1-B",
                "nombre": "Programación 1",
                ...
            }
        ]
    }
    """
    # Este field usa ComisionSerializer para serializar cada comisión
    comisiones = ComisionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Docente
        fields = ['id_docente', 'nombre', 'apellido', 'nombre_completo', 'alias_search', 'comisiones']
        read_only_fields = ['id_docente', 'nombre_completo', 'comisiones']


class ComisionConDocenteSerializer(serializers.ModelSerializer):
    """
    Serializer ANIDADO para Comisión que incluye datos del docente.
    
    En lugar de solo devolver el ID del docente, devuelve sus datos completos.
    
    Útil para:
        - GET /api/comisiones/{id}/ → Ver comisión + docente asignado
        - Cuando necesitas saber quién enseña la comisión
    
    Ejemplo de respuesta JSON:
    {
        "id_comision": 10,
        "codigo": "PROG1-A",
        "nombre": "Programación 1",
        "docente": {
            "id_docente": 1,
            "nombre": "Juan",
            "apellido": "García",
            "nombre_completo": "Juan García",
            "alias_search": "J. García, Garcia"
        },
        "horario": "Lunes-Miércoles 10:00",
        "numero_catedra": 1,
        "cuatrimestre": "1C2025",
        ...
    }
    """
    # Este field usa DocenteSerializer para serializar el docente
    docente = DocenteSerializer(read_only=True)
    
    class Meta:
        model = Comision
        fields = [
            'id_comision', 'codigo', 'nombre', 'docente', 'numero_catedra',
            'horario', 'cuatrimestre', 'modalidad', 'sede', 'es_centro_externo', 'ciclo',
            'mencion_fb', 'ano', 'activa',
            'ultima_actualizacion_scraping', 'fecha_creacion'
        ]
        read_only_fields = ['id_comision', 'fecha_creacion', 'ultima_actualizacion_scraping', 'docente']
