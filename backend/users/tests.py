from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            rol='estudiante'
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
    
    def test_login(self):
        """Test de login exitoso."""
        response = self.client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['rol'], 'estudiante')
    
    def test_me_endpoint(self):
        """Test obtener datos del usuario actual."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['rol'], 'estudiante')
        
    def test_security_students_cannot_list_users(self):
        """Los estudiantes no deberían poder ver la lista de usuarios."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_admin_can_assign_role(self):
        """Un admin debe poder cambiar el rol de un usuario."""
        self.client.force_authenticate(user=self.admin)
        url = f'/api/users/{self.user.pk}/assign_role/'
        data = {'rol': 'colaborador'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.rol, 'colaborador')
    
    def test_student_cannot_assign_role(self):
        """Un estudiante NO debe poder cambiar roles."""
        self.client.force_authenticate(user=self.user)
        url = f'/api/users/{self.user.pk}/assign_role/'
        data = {'rol': 'admin'}
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
