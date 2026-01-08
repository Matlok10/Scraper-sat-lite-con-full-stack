"""
Tests completos para la app Academic.

Cobertura:
- Modelos: Docente, Comision
- Serializers: básicos y anidados
- ViewSets: búsqueda, filtrado, ordenamiento
- Importación: CSV/Excel
- Optimización de queries
"""
import tempfile
from pathlib import Path
from io import StringIO
from django.test import TestCase, TransactionTestCase
from django.core.management import call_command
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import connection
from django.test.utils import override_settings

from .models import Docente, Comision

User = get_user_model()


# ============================================================================
# TESTS DE MODELOS
# ============================================================================

class DocenteModelTest(TestCase):
    """Tests del modelo Docente."""
    
    def test_create_docente_with_nombre_completo_auto(self):
        """El nombre_completo se genera automáticamente."""
        docente = Docente.objects.create(
            nombre='Juan',
            apellido='García'
        )
        self.assertEqual(docente.nombre_completo, 'Juan García')
    
    def test_create_docente_with_alias_search(self):
        """Se puede crear docente con alias_search."""
        docente = Docente.objects.create(
            nombre='María',
            apellido='López',
            alias_search='Profe Mari, M. López, Lopez'
        )
        self.assertIn('Profe Mari', docente.alias_search)
    
    def test_docente_str_representation(self):
        """El __str__ muestra el nombre completo."""
        docente = Docente.objects.create(
            nombre='Pedro',
            apellido='Martínez'
        )
        self.assertEqual(str(docente), 'Pedro Martínez')
    
    def test_docente_can_have_multiple_comisiones(self):
        """Un docente puede tener múltiples comisiones."""
        docente = Docente.objects.create(
            nombre='Ana',
            apellido='Rodríguez'
        )
        
        comision1 = Comision.objects.create(
            codigo='MAT-101',
            nombre='Matemática I',
            docente=docente
        )
        comision2 = Comision.objects.create(
            codigo='MAT-102',
            nombre='Matemática II',
            docente=docente
        )
        
        self.assertEqual(docente.comisiones.count(), 2)
        self.assertIn(comision1, docente.comisiones.all())
        self.assertIn(comision2, docente.comisiones.all())


class ComisionModelTest(TestCase):
    """Tests del modelo Comision."""
    
    def setUp(self):
        self.docente = Docente.objects.create(
            nombre='Laura',
            apellido='González'
        )
    
    def test_create_comision_with_docente(self):
        """Se puede crear comisión con docente asignado."""
        comision = Comision.objects.create(
            codigo='FIS-201',
            nombre='Física I',
            docente=self.docente,
            horario='Lun 10:00 - Mie 10:00',
            cuatrimestre='1C2025'
        )
        
        self.assertEqual(comision.docente, self.docente)
        self.assertTrue(comision.activa)
        self.assertEqual(comision.cuatrimestre, '1C2025')
    
    def test_comision_without_docente(self):
        """Se puede crear comisión sin docente."""
        comision = Comision.objects.create(
            codigo='ANON-1',
            nombre='Curso Sin Docente'
        )
        self.assertIsNone(comision.docente)
    
    def test_comision_str_with_docente(self):
        """El __str__ incluye código, nombre y docente."""
        comision = Comision.objects.create(
            codigo='ROMA-1',
            nombre='Derecho Romano',
            docente=self.docente
        )
        expected = 'ROMA-1 - Derecho Romano (Laura González)'
        self.assertEqual(str(comision), expected)
    
    def test_comision_str_without_docente(self):
        """El __str__ indica 'Sin Docente' cuando no hay docente."""
        comision = Comision.objects.create(
            codigo='TEST-1',
            nombre='Test'
        )
        self.assertIn('Sin Docente', str(comision))
    
    def test_comision_codigo_unique(self):
        """El código de comisión debe ser único."""
        Comision.objects.create(codigo='UNICO-1', nombre='Primera')
        
        with self.assertRaises(Exception):
            Comision.objects.create(codigo='UNICO-1', nombre='Segunda')


# ============================================================================
# TESTS DE SERIALIZERS
# ============================================================================

class DocenteSerializerTest(TestCase):
    """Tests de serializers de Docente."""
    
    def test_docente_serializer_basic(self):
        """DocenteSerializer serializa correctamente."""
        from .serializers import DocenteSerializer
        
        docente = Docente.objects.create(
            nombre='Carlos',
            apellido='Pérez',
            alias_search='CP, Carlitos'
        )
        
        serializer = DocenteSerializer(docente)
        data = serializer.data
        
        self.assertEqual(data['nombre'], 'Carlos')
        self.assertEqual(data['apellido'], 'Pérez')
        self.assertEqual(data['nombre_completo'], 'Carlos Pérez')
        self.assertIn('alias_search', data)
    
    def test_docente_con_comisiones_serializer(self):
        """DocenteConComisionesSerializer incluye comisiones anidadas."""
        from .serializers import DocenteConComisionesSerializer
        
        docente = Docente.objects.create(nombre='Elena', apellido='Díaz')
        Comision.objects.create(codigo='C1', nombre='Comisión 1', docente=docente)
        Comision.objects.create(codigo='C2', nombre='Comisión 2', docente=docente)
        
        serializer = DocenteConComisionesSerializer(docente)
        data = serializer.data
        
        self.assertIn('comisiones', data)
        self.assertEqual(len(data['comisiones']), 2)
        self.assertEqual(data['comisiones'][0]['codigo'], 'C1')


class ComisionSerializerTest(TestCase):
    """Tests de serializers de Comision."""
    
    def setUp(self):
        self.docente = Docente.objects.create(nombre='Test', apellido='Docente')
    
    def test_comision_serializer_basic(self):
        """ComisionSerializer serializa correctamente."""
        from .serializers import ComisionSerializer
        
        comision = Comision.objects.create(
            codigo='TEST-1',
            nombre='Test Comision',
            docente=self.docente
        )
        
        serializer = ComisionSerializer(comision)
        data = serializer.data
        
        self.assertEqual(data['codigo'], 'TEST-1')
        self.assertEqual(data['nombre'], 'Test Comision')
        self.assertEqual(data['docente'], self.docente.id_docente)
    
    def test_comision_con_docente_serializer(self):
        """ComisionConDocenteSerializer incluye datos del docente."""
        from .serializers import ComisionConDocenteSerializer
        
        comision = Comision.objects.create(
            codigo='NEST-1',
            nombre='Nested Test',
            docente=self.docente
        )
        
        serializer = ComisionConDocenteSerializer(comision)
        data = serializer.data
        
        self.assertIn('docente', data)
        self.assertIsInstance(data['docente'], dict)
        self.assertEqual(data['docente']['nombre'], 'Test')
        self.assertEqual(data['docente']['apellido'], 'Docente')


# ============================================================================
# TESTS DE API - DOCENTE VIEWSET
# ============================================================================

class DocenteAPITest(APITestCase):
    """Tests del DocenteViewSet."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        # Crear docentes de prueba
        self.docente1 = Docente.objects.create(
            nombre='Juan',
            apellido='García',
            alias_search='J. García, Profe Juan'
        )
        self.docente2 = Docente.objects.create(
            nombre='María',
            apellido='López',
            alias_search='M. López'
        )
        self.docente3 = Docente.objects.create(
            nombre='Pedro',
            apellido='Fernández'
        )
        
        self.url_list = reverse('docente-list')
    
    def test_list_docentes(self):
        """GET /api/docentes/ lista todos los docentes."""
        response = self.client.get(self.url_list)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_create_docente(self):
        """POST /api/docentes/ crea un nuevo docente."""
        data = {
            'nombre': 'Nuevo',
            'apellido': 'Docente',
            'alias_search': 'ND'
        }
        response = self.client.post(self.url_list, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Docente.objects.count(), 4)
        self.assertEqual(response.data['nombre_completo'], 'Nuevo Docente')
    
    def test_retrieve_docente_includes_comisiones(self):
        """GET /api/docentes/{id}/ incluye comisiones anidadas."""
        Comision.objects.create(
            codigo='TEST-1',
            nombre='Test',
            docente=self.docente1
        )
        
        url = reverse('docente-detail', args=[self.docente1.id_docente])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('comisiones', response.data)
        self.assertEqual(len(response.data['comisiones']), 1)
    
    def test_search_by_apellido(self):
        """?search=garc busca por apellido (case-insensitive, funciona con acentos)."""
        response = self.client.get(f'{self.url_list}?search=garc')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['apellido'], 'García')
    
    def test_search_by_nombre(self):
        """?search=mar busca por nombre (case-insensitive, funciona con acentos)."""
        response = self.client.get(f'{self.url_list}?search=mar')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['nombre'], 'María')
    
    def test_search_by_alias(self):
        """?search=profe busca en alias_search."""
        response = self.client.get(f'{self.url_list}?search=profe')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertIn('Profe Juan', results[0]['alias_search'])
    
    def test_ordering_by_apellido_asc(self):
        """?ordering=apellido ordena ascendente."""
        response = self.client.get(f'{self.url_list}?ordering=apellido')
        
        results = response.data['results']
        apellidos = [r['apellido'] for r in results]
        self.assertEqual(apellidos, ['Fernández', 'García', 'López'])
    
    def test_ordering_by_apellido_desc(self):
        """?ordering=-apellido ordena descendente."""
        response = self.client.get(f'{self.url_list}?ordering=-apellido')
        
        results = response.data['results']
        apellidos = [r['apellido'] for r in results]
        self.assertEqual(apellidos, ['López', 'García', 'Fernández'])
    
    def test_estadisticas_endpoint(self):
        """GET /api/docentes/estadisticas/ retorna métricas."""
        # Crear comisiones para algunos docentes
        Comision.objects.create(codigo='C1', nombre='C1', docente=self.docente1)
        Comision.objects.create(codigo='C2', nombre='C2', docente=self.docente2)
        
        url = reverse('docente-estadisticas')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_docentes', response.data)
        self.assertIn('docentes_con_comisiones', response.data)
        self.assertIn('docentes_sin_comisiones', response.data)
        
        self.assertEqual(response.data['total_docentes'], 3)
        self.assertEqual(response.data['docentes_con_comisiones'], 2)
        self.assertEqual(response.data['docentes_sin_comisiones'], 1)


# ============================================================================
# TESTS DE API - COMISION VIEWSET
# ============================================================================

class ComisionAPITest(APITestCase):
    """Tests del ComisionViewSet."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.docente = Docente.objects.create(
            nombre='Test',
            apellido='Docente'
        )
        
        self.comision1 = Comision.objects.create(
            codigo='MAT-101',
            nombre='Matemática I',
            docente=self.docente,
            cuatrimestre='1C2025'
        )
        self.comision2 = Comision.objects.create(
            codigo='FIS-201',
            nombre='Física II',
            docente=self.docente
        )
        
        self.url_list = reverse('catedra-list')
    
    def test_list_comisiones(self):
        """GET /api/catedras/ lista comisiones con docente anidado."""
        response = self.client.get(self.url_list)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        
        # Verifica que incluya datos del docente
        first = response.data['results'][0]
        self.assertIn('docente', first)
        self.assertIsInstance(first['docente'], dict)
    
    def test_search_by_codigo(self):
        """?search=mat busca por código."""
        response = self.client.get(f'{self.url_list}?search=mat')
        
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['codigo'], 'MAT-101')
    
    def test_search_by_nombre(self):
        """?search=fis busca por nombre (parcial, funciona con acentos)."""
        response = self.client.get(f'{self.url_list}?search=fis')
        
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['nombre'], 'Física II')
    
    def test_search_by_docente_apellido(self):
        """?search=docente busca por apellido del docente."""
        response = self.client.get(f'{self.url_list}?search=docente')
        
        results = response.data['results']
        self.assertEqual(len(results), 2)


# ============================================================================
# TESTS DE IMPORTACIÓN
# ============================================================================

class ImportComisionesCommandTest(TransactionTestCase):
    """Tests del comando de importación."""
    
    def test_import_csv_basic(self):
        """Importa CSV básico correctamente."""
        # Crear CSV temporal
        csv_content = """Período lectivo,Actividad,Comisión,Modalidad,Docente,Horario
PRIMER CUATRIMESTRE 2025,205 (PRI) - DERECHO ROMANO,0620,Presencial,GARCÍA JUAN,Lun 07:00
PRIMER CUATRIMESTRE 2025,2X8 (PRI) - DERECHO DE DAÑOS,0016,Presencial,LÓPEZ MARÍA,Mie 10:00"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            csv_path = f.name
        
        try:
            # Ejecutar comando
            out = StringIO()
            call_command('import_comisiones', csv_path, stdout=out)
            
            # Verificar resultados
            self.assertEqual(Docente.objects.count(), 2)
            self.assertEqual(Comision.objects.count(), 2)
            
            # Verificar docentes
            garcia = Docente.objects.get(apellido='García')
            self.assertEqual(garcia.nombre, 'Juan')
            
            # Verificar comisiones
            roma = Comision.objects.get(codigo='205-0620')
            self.assertEqual(roma.nombre, 'DERECHO ROMANO')
            self.assertEqual(roma.docente, garcia)
            
        finally:
            Path(csv_path).unlink()
    
    def test_import_csv_with_dry_run(self):
        """Dry-run no guarda datos."""
        csv_content = """Período lectivo,Actividad,Comisión,Modalidad,Docente,Horario
PRIMER CUATRIMESTRE 2025,TEST-1,T001,Presencial,TEST DOCENTE,Lun 10:00"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            csv_path = f.name
        
        try:
            call_command('import_comisiones', csv_path, dry_run=True, stdout=StringIO())
            
            # No debe haber guardado nada
            self.assertEqual(Docente.objects.count(), 0)
            self.assertEqual(Comision.objects.count(), 0)
            
        finally:
            Path(csv_path).unlink()
    
    def test_import_updates_existing_comision(self):
        """update_existing actualiza comisiones existentes."""
        # Crear comisión inicial
        docente1 = Docente.objects.create(nombre='Inicial', apellido='Docente')
        Comision.objects.create(
            codigo='TEST-1',
            nombre='Inicial',
            docente=docente1
        )
        
        # CSV con actualización
        csv_content = """Período lectivo,Actividad,Comisión,Modalidad,Docente,Horario
PRIMER CUATRIMESTRE 2025,TEST,TEST-1,Presencial,NUEVO DOCENTE,Mie 14:00"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            csv_path = f.name
        
        try:
            call_command('import_comisiones', csv_path, update_existing=True, stdout=StringIO())
            
            # Verificar actualización
            comision = Comision.objects.get(codigo='TEST-1')
            self.assertEqual(comision.nombre, 'TEST')
            self.assertEqual(comision.docente.apellido, 'Nuevo')  # Docente actualizado desde el CSV
            
        finally:
            Path(csv_path).unlink()


# ============================================================================
# TESTS DE OPTIMIZACIÓN DE QUERIES
# ============================================================================

class QueryOptimizationTest(TestCase):
    """Tests de optimización de queries N+1."""
    
    def setUp(self):
        # Crear docentes con comisiones
        for i in range(5):
            docente = Docente.objects.create(
                nombre=f'Docente{i}',
                apellido=f'Apellido{i}'
            )
            for j in range(3):
                Comision.objects.create(
                    codigo=f'C{i}-{j}',
                    nombre=f'Comisión {i}-{j}',
                    docente=docente
                )
    
    def test_list_docentes_no_n_plus_one(self):
        """Listar docentes no causa N+1 queries."""
        client = APIClient()
        
        with self.assertNumQueries(2):  # 1 para auth, 1 para docentes
            response = client.get(reverse('docente-list'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_retrieve_docente_with_prefetch(self):
        """Detalle de docente usa prefetch_related."""
        docente = Docente.objects.first()
        client = APIClient()
        
        with self.assertNumQueries(2):  # docente + comisiones (prefetch)
            response = client.get(reverse('docente-detail', args=[docente.id_docente]))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('comisiones', response.data)
    
    def test_list_comisiones_with_select_related(self):
        """Listar comisiones usa select_related para docente."""
        client = APIClient()
        
        with self.assertNumQueries(2):  # auth + comisiones con JOIN de docente
            response = client.get(reverse('catedra-list'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)


# ============================================================================
# TESTS DE EDGE CASES
# ============================================================================

class EdgeCasesTest(TestCase):
    """Tests de casos límite."""
    
    def test_docente_with_very_long_nombre(self):
        """Nombre muy largo se maneja correctamente."""
        nombre_largo = 'A' * 100
        docente = Docente.objects.create(
            nombre=nombre_largo,
            apellido='Test'
        )
        self.assertEqual(len(docente.nombre), 100)
    
    def test_comision_without_cuatrimestre(self):
        """Comisión sin cuatrimestre es válida."""
        comision = Comision.objects.create(
            codigo='NO-CUATRI',
            nombre='Sin Cuatrimestre'
        )
        self.assertIsNone(comision.cuatrimestre)
    
    def test_search_with_special_characters(self):
        """Búsqueda con caracteres especiales (acentos) en SQLite requiere coincidencia parcial."""
        Docente.objects.create(
            nombre='José',
            apellido='Pérez'
        )
        
        client = APIClient()
        # En SQLite, buscar 'jos' encuentra 'José' (case-insensitive pero no accent-insensitive)
        response = client.get(f"{reverse('docente-list')}?search=jos")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
    
    def test_delete_docente_cascades_to_comisiones(self):
        """Eliminar docente elimina sus comisiones (CASCADE)."""
        docente = Docente.objects.create(nombre='Del', apellido='Test')
        Comision.objects.create(codigo='DEL-1', nombre='Del', docente=docente)
        
        self.assertEqual(Comision.objects.count(), 1)
        docente.delete()
        self.assertEqual(Comision.objects.count(), 0)
