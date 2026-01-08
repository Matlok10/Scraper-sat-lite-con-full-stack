"""
Views para la app academic.

Incluye ViewSets con capacidades de búsqueda y filtrado avanzado.
"""
import io
import tempfile
from pathlib import Path
from django.core.management.base import CommandError
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Docente, Comision
from .serializers import (
    DocenteSerializer, 
    ComisionSerializer,
    DocenteConComisionesSerializer,
    ComisionConDocenteSerializer
)
from academic.management.commands import import_comisiones


# ============================================================================
# DOCENTE VIEWSET - Con búsqueda avanzada
# ============================================================================

class DocenteViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar docentes con búsqueda avanzada.
    
    **Funcionalidades:**
    
    1. **CRUD completo:** 
       - GET /api/docentes/ → Listar todos
       - GET /api/docentes/{id}/ → Ver detalle con comisiones
       - POST /api/docentes/ → Crear docente
       - PUT/PATCH /api/docentes/{id}/ → Actualizar
       - DELETE /api/docentes/{id}/ → Eliminar
    
    2. **Búsqueda avanzada:**
       - ?search=García → Busca por nombre, apellido, alias_search
       - ?search=Juan G → Búsqueda flexible
       - ?ordering=nombre → Ordenar resultados
       - ?ordering=-apellido → Orden descendente
    
    3. **Ejemplos de uso:**
       ```
       GET /api/docentes/?search=garcia
       → Encuentra "García", "Garcia", "J. García"
       
       GET /api/docentes/?search=prof juan
       → Encuentra "Prof. Juan García" si está en alias_search
       
       GET /api/docentes/?ordering=apellido
       → Ordena alfabéticamente por apellido
       ```
    
    **Serializers utilizados:**
    - Lista (GET /api/docentes/): DocenteSerializer (básico, sin comisiones)
    - Detalle (GET /api/docentes/1/): DocenteConComisionesSerializer (con comisiones)
    - Escritura (POST/PUT/PATCH): DocenteSerializer
    """
    
    queryset = Docente.objects.all()
    
    # Configuración de filtros de búsqueda
    # SearchFilter permite buscar en múltiples campos
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # ¿En qué campos puede buscar el usuario?
    # ^ = búsqueda exacta al inicio
    # @ = búsqueda de texto completo (si está disponible en la BD)
    # Sin prefijo = búsqueda parcial (contiene)
    search_fields = [
        'nombre',           # Busca en el nombre
        'apellido',         # Busca en el apellido
        'nombre_completo',  # Busca en nombre completo
        'alias_search',     # Busca en aliases (muy útil!)
    ]
    
    # ¿Por qué campos se puede ordenar?
    ordering_fields = ['nombre', 'apellido', 'nombre_completo', 'id_docente']
    ordering = ['apellido', 'nombre']  # Orden por defecto
    
    def get_serializer_class(self):
        """
        Selecciona el serializer según la acción.
        
        ¿Por qué esto es importante?
        - Al LISTAR muchos docentes → No necesitas las comisiones (sería lento)
        - Al VER UN docente específico → Sí quieres ver sus comisiones
        
        Esto se llama "optimización de queries" y hace tu API más rápida.
        """
        if self.action == 'retrieve':  # GET /api/docentes/1/
            return DocenteConComisionesSerializer
        return DocenteSerializer
    
    def get_queryset(self):
        """
        Optimiza las consultas a la base de datos.
        
        ¿Qué hace prefetch_related?
        Sin esto: Si listas 100 docentes y cada uno tiene comisiones,
                  Django haría 101 queries (1 + 100)
        
        Con esto: Django hace solo 2 queries (1 para docentes, 1 para todas las comisiones)
        
        Esto se llama "N+1 problem" y es muy importante optimizarlo.
        """
        queryset = super().get_queryset()
        
        # Si estamos viendo el detalle, incluye las comisiones relacionadas
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('comisiones')
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, _request):
        """
        Endpoint personalizado para obtener estadísticas.
        
        **Uso:**
        GET /api/docentes/estadisticas/
        
        **Respuesta:**
        {
            "total_docentes": 45,
            "docentes_con_comisiones": 40,
            "docentes_sin_comisiones": 5,
            "promedio_comisiones_por_docente": 2.3
        }
        
        ¿Qué es @action?
        - detail=False → Se aplica a la colección (no a un docente específico)
        - methods=['get'] → Solo permite GET
        - La URL se genera automáticamente: /api/docentes/estadisticas/
        """
        total = Docente.objects.count()
        con_comisiones = Docente.objects.filter(comisiones__isnull=False).distinct().count()
        
        return Response({
            'total_docentes': total,
            'docentes_con_comisiones': con_comisiones,
            'docentes_sin_comisiones': total - con_comisiones,
        })


# ============================================================================
# COMISION VIEWSET - Mejorado con serializers anidados
# ============================================================================

class ComisionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar comisiones.
    
    **Funcionalidades:**
    - Lista todas las comisiones con información del docente
    - Búsqueda por código, nombre, docente
    - Filtrado por activa/inactiva
    - Ordenamiento personalizado
    
    **Ejemplos:**
    ```
    GET /api/catedras/?search=programacion
    → Busca comisiones con "programacion" en nombre o código
    
    GET /api/catedras/?search=garcia
    → Busca comisiones donde el docente se llame García
    
    GET /api/catedras/?ordering=codigo
    → Ordena por código de comisión
    ```
    """
    
    queryset = Comision.objects.all()
    
    # Configuración de búsqueda
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        'codigo',
        'nombre',
        'docente__nombre',      # Busca en el nombre del docente relacionado
        'docente__apellido',    # Busca en el apellido del docente
        'cuatrimestre',
    ]
    ordering_fields = ['codigo', 'nombre', 'activa', 'ano']
    ordering = ['codigo']
    
    def get_serializer_class(self):
        """
        Usa serializer anidado para lectura, básico para escritura.
        
        ¿Por qué?
        - Lectura: Quieres ver los datos del docente
        - Escritura: Solo envías el ID del docente
        """
        if self.action in ['retrieve', 'list']:
            return ComisionConDocenteSerializer
        return ComisionSerializer
    
    def get_queryset(self):
        """
        Optimiza queries incluyendo el docente relacionado.
        
        select_related es como prefetch_related pero para ForeignKey.
        """
        queryset = super().get_queryset()
        
        # Siempre incluye el docente para evitar queries adicionales
        queryset = queryset.select_related('docente')
        
        return queryset

    def create(self, request, *args, **kwargs):
        """Crear comisión con validación explícita para ver errores claramente en tests."""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], url_path='crear-manual', permission_classes=[AllowAny])
    def crear_manual(self, request):
        """Crea o actualiza una comisión a partir de datos simples (sin ID de docente)."""
        data = request.data

        codigo = (data.get('codigo') or '').strip()
        nombre = (data.get('nombre') or '').strip()
        docente_nombre = (data.get('docente_nombre') or '').strip()
        docente_apellido = (data.get('docente_apellido') or '').strip()
        docente_completo = (data.get('docente_completo') or '').strip()
        ciclo = (data.get('ciclo') or '').strip().upper()

        if not docente_completo and (docente_nombre or docente_apellido):
            docente_completo = f"{docente_nombre} {docente_apellido}".strip()

        if not codigo or not nombre or not docente_completo:
            return Response(
                {'detail': 'Código, nombre y docente son obligatorios.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if ciclo and ciclo not in {'CPO', 'CPC'}:
            return Response(
                {'detail': 'El ciclo debe ser CPO o CPC.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Normalizar nombre y apellido
        if not docente_apellido or not docente_nombre:
            partes = docente_completo.split()
            if len(partes) >= 2:
                docente_apellido = partes[0]
                docente_nombre = ' '.join(partes[1:])
            else:
                docente_apellido = docente_completo
                docente_nombre = ''

        docente, _created = Docente.objects.get_or_create(
            nombre_completo__iexact=docente_completo,
            defaults={
                'nombre': docente_nombre.title(),
                'apellido': docente_apellido.title(),
                'nombre_completo': docente_completo.title(),
            }
        )

        def to_int(value):
            try:
                return int(value)
            except (TypeError, ValueError):
                return None

        horario = (data.get('horario') or '').strip()
        cuatrimestre = (data.get('cuatrimestre') or '').strip()
        modalidad = (data.get('modalidad') or '').strip() or None
        sede = (data.get('sede') or '').strip()
        numero_catedra = to_int(data.get('numero_catedra'))
        ano = to_int(data.get('ano'))
        es_centro_externo = str(data.get('es_centro_externo') or '').lower() in {'1', 'true', 'yes', 'si', 'sí', 'on'}

        # Consolidar por código+docente+cuatrimestre+sede: mantener el horario más descriptivo
        existentes = list(Comision.objects.filter(
            codigo=codigo,
            docente=docente,
            cuatrimestre=cuatrimestre,
            sede=sede,
        ))

        if existentes:
            # Elegir el registro con horario más largo entre existentes y el nuevo
            candidato = max(
                existentes + [Comision(horario=horario or '')],
                key=lambda c: len(c.horario or '')
            )

            # Actualizar el elegido; si el elegido es nuevo, tomamos el primero de la lista
            target = candidato if candidato.id_comision else existentes[0]
            target.horario = candidato.horario or horario
            target.nombre = nombre[:200]
            target.modalidad = modalidad if modalidad in ['Presencial', 'Remota', 'Híbrida'] else None
            target.numero_catedra = numero_catedra
            target.ano = ano
            target.es_centro_externo = es_centro_externo
            target.ciclo = ciclo
            target.activa = True
            target.save()

            # Eliminar otros duplicados si los hay
            for item in existentes:
                if item.id_comision != target.id_comision:
                    item.delete()
            comision = target
            created = False
        else:
            comision = Comision.objects.create(
                codigo=codigo,
                docente=docente,
                horario=horario,
                cuatrimestre=cuatrimestre,
                sede=sede,
                nombre=nombre[:200],
                modalidad=modalidad if modalidad in ['Presencial', 'Remota', 'Híbrida'] else None,
                numero_catedra=numero_catedra,
                ano=ano,
                es_centro_externo=es_centro_externo,
                ciclo=ciclo,
                activa=True,
            )
            created = True

        serializer = ComisionConDocenteSerializer(comision)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response({'created': created, 'catedra': serializer.data}, status=status_code)

    @action(detail=False, methods=['post'], url_path='importar', permission_classes=[AllowAny])
    def importar(self, request):
        """Importa comisiones desde CSV/XLS/XLSX cargado vía web."""
        upload = request.FILES.get('file')
        if not upload:
            return Response({'detail': 'No se envió archivo.'}, status=status.HTTP_400_BAD_REQUEST)

        ciclo = (request.data.get('ciclo') or '').strip().upper()
        if ciclo and ciclo not in {'CPO', 'CPC'}:
            return Response({'detail': 'El ciclo debe ser CPO o CPC.'}, status=status.HTTP_400_BAD_REQUEST)

        extension = Path(upload.name).suffix.lower()
        if extension not in {'.csv', '.xlsx', '.xls'}:
            return Response({'detail': 'Formato no soportado. Use CSV, XLS o XLSX.'}, status=status.HTTP_400_BAD_REQUEST)

        update_existing = str(request.data.get('update_existing') or '').lower() in {'1', 'true', 'yes', 'si', 'sí', 'on'}

        with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as tmp:
            for chunk in upload.chunks():
                tmp.write(chunk)
            temp_path = Path(tmp.name)

        cmd = import_comisiones.Command()
        log_buffer = io.StringIO()
        cmd.stdout = log_buffer
        cmd.stderr = log_buffer

        try:
            cmd.handle(file_path=str(temp_path), dry_run=False, update_existing=update_existing, ciclo=ciclo)
            result = getattr(cmd, 'last_run_result', {}) or {}
        except CommandError as exc:
            temp_path.unlink(missing_ok=True)
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            temp_path.unlink(missing_ok=True)

        return Response({
            'status': 'ok',
            'stats': result.get('stats', {}),
            'duplicates': result.get('duplicates', {}),
            'dry_run': result.get('dry_run', False),
            'log': [line for line in log_buffer.getvalue().splitlines() if line.strip()],
        })
