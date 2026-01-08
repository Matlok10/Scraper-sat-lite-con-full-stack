from django.test import TestCase
from academic.models import Comision, Docente
from scraping.models import Grupos, Post_Scrapeado, Tarea_Scrapeo, Sesion_Scraping
from recommendations.models import Recomendacion
from django.contrib.auth import get_user_model

User = get_user_model()

class AcademicModelTest(TestCase):

    def setUp(self):
        self.docente = Docente.objects.create(
            nombre="Juan",
            apellido="Perez",
            alias_search="jperez"
        )
        self.comision = Comision.objects.create(
            codigo="ALG-1",
            nombre="Algebra",
            docente=self.docente,
            activa=True
        )

    def test_docente_creation(self):
        self.assertEqual(self.docente.nombre_completo, "Juan Perez")
        self.assertTrue(isinstance(self.docente, Docente))
        self.assertEqual(str(self.docente), "Juan Perez")

    def test_comision_creation(self):
        self.assertTrue(isinstance(self.comision, Comision))
        self.assertEqual(self.comision.docente, self.docente)
        self.assertEqual(str(self.comision), "ALG-1 - Algebra (Juan Perez)")
    
    def test_comision_without_docente(self):
        comision_anonima = Comision.objects.create(
            codigo="ANON-1",
            nombre="Curso Anonimo"
        )
        self.assertIsNone(comision_anonima.docente)
        self.assertIn("Sin Docente", str(comision_anonima))


class RecomendacionModelTest(TestCase):

    def setUp(self):
        # Create dependencies
        self.user = User.objects.create_user(username='testuser', password='password')
        self.docente = Docente.objects.create(nombre="Ana", apellido="Gomez")
        self.comision = Comision.objects.create(
            codigo="FIS-1", 
            nombre="Fisica I", 
            docente=self.docente
        )
        self.grupo = Grupos.objects.create(nombre="Grupo Test", url="http://fb.com/test")
        self.post = Post_Scrapeado.objects.create(
            post_id="12345", 
            grupo=self.grupo, 
            texto="Un gran curso se aprende mucho"
        )
        
        self.recomendacion = Recomendacion.objects.create(
            comision=self.comision,
            post_origen=self.post,
            texto="Un gran curso se aprende mucho",
            sentimiento="positivo",
            confianza=0.95,
            prob_aprobar="alto",
            asistencia=True
        )

    def test_recomendacion_creation(self):
        self.assertTrue(isinstance(self.recomendacion, Recomendacion))
        self.assertEqual(self.recomendacion.comision, self.comision)
        self.assertEqual(self.recomendacion.sentimiento, "positivo")
        self.assertEqual(self.recomendacion.prob_aprobar, "alto")
        self.assertTrue(self.recomendacion.asistencia)

    def test_recomendacion_str(self):
        expected_str = f"{self.comision.codigo} - positivo (0.95)"
        self.assertEqual(str(self.recomendacion), expected_str)
