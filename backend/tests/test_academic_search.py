from typing import Any, Dict, cast
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from academic.models import Docente, Comision

User = get_user_model()


class DocenteSearchAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apiuser_doc', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Docentes con distintos campos para búsquedas
        self.docente_garcia = Docente.objects.create(
            nombre='Maria',
            apellido='García',
            alias_search='profe roma garcia'
        )
        self.docente_fernandez = Docente.objects.create(
            nombre='Juan',
            apellido='Fernandez',
            alias_search='juan fer'
        )

        # Comisiones asociadas al primer docente (para detalle)
        self.comision = Comision.objects.create(
            codigo='ROMA-101',
            nombre='Derecho Romano',
            docente=self.docente_garcia,
            horario='Lun 07:00 - Jue 07:00'
        )

        self.url_list = reverse('docente-list')

    def test_search_by_apellido(self):
        response = cast(Response, self.client.get(f"{self.url_list}?search=garc"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(d['apellido'] == 'García' for d in response.data['results']))
        self.assertFalse(any(d['apellido'] == 'Fernandez' for d in response.data['results']))

    def test_search_by_alias(self):
        response = cast(Response, self.client.get(f"{self.url_list}?search=roma"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(d['id_docente'] == self.docente_garcia.id_docente for d in response.data['results']))

    def test_retrieve_includes_comisiones(self):
        url_detail = reverse('docente-detail', args=[self.docente_garcia.id_docente])
        response = cast(Response, self.client.get(url_detail))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = cast(Dict[str, Any], response.data)
        self.assertIn('comisiones', data)
        self.assertEqual(len(data['comisiones']), 1)
        self.assertEqual(data['comisiones'][0]['codigo'], 'ROMA-101')


class ComisionSearchAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apiuser_com', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.docente = Docente.objects.create(nombre='Laura', apellido='Lopez', alias_search='laulo')
        self.comision1 = Comision.objects.create(
            codigo='CIVIL-1',
            nombre='Derecho Civil',
            docente=self.docente,
        )
        self.comision2 = Comision.objects.create(
            codigo='PENAL-1',
            nombre='Derecho Penal',
            docente=self.docente,
        )

        self.url_list = reverse('catedra-list')

    def test_search_by_docente_lastname(self):
        response = cast(Response, self.client.get(f"{self.url_list}?search=lopez"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        codes = [c['codigo'] for c in response.data['results']]
        self.assertIn('CIVIL-1', codes)
        self.assertIn('PENAL-1', codes)

    def test_search_by_codigo(self):
        response = cast(Response, self.client.get(f"{self.url_list}?search=penal"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(c['codigo'] == 'PENAL-1' for c in response.data['results']))
