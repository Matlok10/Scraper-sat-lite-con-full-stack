"""
Tests completos para la app Users (Fase 1)
Incluye: Autenticación, Roles, Permisos, Gamificación
"""
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserModelTest(TestCase):
    """Tests del modelo User personalizado"""
    
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
    
    def test_create_user_with_default_role(self):
        """Un usuario nuevo debe tener rol 'estudiante' por defecto"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.rol, 'estudiante')
        self.assertEqual(user.puntos, 0)
        self.assertEqual(user.contribuciones_aprobadas, 0)
        self.assertFalse(user.puede_scrapear)
    
    def test_create_user_with_custom_role(self):
        """Se puede crear un usuario con un rol específico"""
        user = User.objects.create_user(
            username='colaborador1',
            email='colab@example.com',
            password='pass123',
            rol='colaborador'
        )
        self.assertEqual(user.rol, 'colaborador')
    
    def test_user_string_representation(self):
        """El __str__ del usuario debe incluir username, email y rol"""
        user = User.objects.create_user(**self.user_data)
        expected = f"{user.username} ({user.email}) - {user.rol}"
        self.assertEqual(str(user), expected)
    
    def test_rol_choices_validation(self):
        """Solo se pueden asignar roles válidos"""
        user = User.objects.create_user(**self.user_data)
        valid_roles = ['estudiante', 'colaborador', 'moderador', 'admin']
        
        for rol in valid_roles:
            user.rol = rol
            user.save()
            user.refresh_from_db()
            self.assertEqual(user.rol, rol)
    
    def test_gamification_fields(self):
        """Los campos de gamificación funcionan correctamente"""
        user = User.objects.create_user(**self.user_data)
        
        # Simular aprobación de contribución
        user.contribuciones_aprobadas += 1
        user.puntos += 10
        user.save()
        
        user.refresh_from_db()
        self.assertEqual(user.contribuciones_aprobadas, 1)
        self.assertEqual(user.puntos, 10)
    
    def test_scraping_metadata_fields(self):
        """Los campos de metadata de scraping funcionan"""
        user = User.objects.create_user(**self.user_data, rol='colaborador')
        
        user.puede_scrapear = True
        user.sesiones_scraping_activas = 2
        user.save()
        
        user.refresh_from_db()
        self.assertTrue(user.puede_scrapear)
        self.assertEqual(user.sesiones_scraping_activas, 2)


class UserAuthenticationAPITest(APITestCase):
    """Tests de autenticación (login/logout)"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='authuser',
            email='auth@example.com',
            password='authpass123',
            rol='estudiante'
        )
        self.login_url = '/api/auth/login/'
        self.logout_url = '/api/auth/logout/'
    
    def test_login_success(self):
        """Login exitoso debe retornar token y datos del usuario"""
        response = self.client.post(self.login_url, {
            'username': 'authuser',
            'password': 'authpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('rol', response.data)
        
        self.assertEqual(response.data['username'], 'authuser')
        self.assertEqual(response.data['email'], 'auth@example.com')
        self.assertEqual(response.data['rol'], 'estudiante')
    
    def test_login_invalid_credentials(self):
        """Login con credenciales incorrectas debe fallar"""
        response = self.client.post(self.login_url, {
            'username': 'authuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_creates_token(self):
        """Login debe crear un token en la base de datos"""
        tokens_before = Token.objects.count()
        
        response = self.client.post(self.login_url, {
            'username': 'authuser',
            'password': 'authpass123'
        })
        
        tokens_after = Token.objects.count()
        self.assertEqual(tokens_after, tokens_before + 1)
        
        # Verificar que el token existe para el usuario
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data['token'], token.key)
    
    def test_logout_success(self):
        """Logout debe eliminar el token del usuario"""
        # Crear token
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        
        response = self.client.post(self.logout_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar que el token fue eliminado
        self.assertFalse(Token.objects.filter(user=self.user).exists())
    
    def test_logout_requires_authentication(self):
        """Logout sin autenticación debe fallar"""
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserViewSetAPITest(APITestCase):
    """Tests del UserViewSet (CRUD y acciones personalizadas)"""
    
    def setUp(self):
        # Crear usuarios de prueba
        self.estudiante = User.objects.create_user(
            username='estudiante1',
            email='estudiante@example.com',
            password='pass123',
            rol='estudiante'
        )
        
        self.colaborador = User.objects.create_user(
            username='colaborador1',
            email='colaborador@example.com',
            password='pass123',
            rol='colaborador',
            puntos=50
        )
        
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        self.users_url = '/api/users/'
        self.me_url = '/api/users/me/'
    
    def test_me_endpoint_authenticated(self):
        """Endpoint /me/ debe retornar datos del usuario autenticado"""
        self.client.force_authenticate(user=self.estudiante)
        response = self.client.get(self.me_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'estudiante1')
        self.assertEqual(response.data['email'], 'estudiante@example.com')
        self.assertEqual(response.data['rol'], 'estudiante')
        self.assertEqual(response.data['puntos'], 0)
    
    def test_me_endpoint_unauthenticated(self):
        """Endpoint /me/ sin autenticación debe fallar"""
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_users_as_student(self):
        """Estudiantes NO pueden listar usuarios"""
        self.client.force_authenticate(user=self.estudiante)
        response = self.client.get(self.users_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_list_users_as_admin(self):
        """Admins SÍ pueden listar usuarios"""
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.users_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 3)
    
    def test_retrieve_user_as_authenticated(self):
        """Usuarios autenticados pueden ver detalles de otros usuarios"""
        self.client.force_authenticate(user=self.estudiante)
        url = f'/api/users/{self.colaborador.pk}/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'colaborador1')
        self.assertEqual(response.data['puntos'], 50)
    
    def test_update_user_as_student(self):
        """Estudiantes NO pueden actualizar usuarios"""
        self.client.force_authenticate(user=self.estudiante)
        url = f'/api/users/{self.estudiante.pk}/'
        response = self.client.patch(url, {'first_name': 'Juan'})
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_user_as_admin(self):
        """Admins SÍ pueden actualizar usuarios"""
        self.client.force_authenticate(user=self.admin)
        url = f'/api/users/{self.estudiante.pk}/'
        response = self.client.patch(url, {'first_name': 'Juan'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.estudiante.refresh_from_db()
        self.assertEqual(self.estudiante.first_name, 'Juan')
    
    def test_delete_user_as_student(self):
        """Estudiantes NO pueden eliminar usuarios"""
        self.client.force_authenticate(user=self.estudiante)
        url = f'/api/users/{self.colaborador.pk}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_user_as_admin(self):
        """Admins SÍ pueden eliminar usuarios"""
        user_to_delete = User.objects.create_user(
            username='deleteme',
            email='delete@example.com',
            password='pass123'
        )
        
        self.client.force_authenticate(user=self.admin)
        url = f'/api/users/{user_to_delete.pk}/'
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=user_to_delete.pk).exists())


class UserRoleManagementAPITest(APITestCase):
    """Tests de asignación de roles"""
    
    def setUp(self):
        self.estudiante = User.objects.create_user(
            username='estudiante1',
            email='estudiante@example.com',
            password='pass123',
            rol='estudiante'
        )
        
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
    
    def test_assign_role_as_admin(self):
        """Admin puede asignar roles"""
        self.client.force_authenticate(user=self.admin)
        url = f'/api/users/{self.estudiante.pk}/assign_role/'
        response = self.client.post(url, {'rol': 'colaborador'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Rol actualizado', response.data['status'])
        
        self.estudiante.refresh_from_db()
        self.assertEqual(self.estudiante.rol, 'colaborador')
    
    def test_assign_role_as_student(self):
        """Estudiantes NO pueden asignar roles"""
        self.client.force_authenticate(user=self.estudiante)
        url = f'/api/users/{self.estudiante.pk}/assign_role/'
        response = self.client.post(url, {'rol': 'admin'})
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_assign_invalid_role(self):
        """No se puede asignar un rol inválido"""
        self.client.force_authenticate(user=self.admin)
        url = f'/api/users/{self.estudiante.pk}/assign_role/'
        response = self.client.post(url, {'rol': 'superuser'})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    def test_assign_all_valid_roles(self):
        """Se pueden asignar todos los roles válidos"""
        self.client.force_authenticate(user=self.admin)
        url = f'/api/users/{self.estudiante.pk}/assign_role/'
        
        valid_roles = ['estudiante', 'colaborador', 'moderador', 'admin']
        
        for rol in valid_roles:
            response = self.client.post(url, {'rol': rol})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            
            self.estudiante.refresh_from_db()
            self.assertEqual(self.estudiante.rol, rol)


class UserSerializerTest(TestCase):
    """Tests del UserSerializer"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='serializertest',
            email='serializer@example.com',
            password='pass123',
            rol='colaborador',
            puntos=100,
            contribuciones_aprobadas=5
        )
    
    def test_serializer_exposes_correct_fields(self):
        """El serializer debe exponer los campos correctos"""
        from users.serializers import UserSerializer
        
        serializer = UserSerializer(self.user)
        data = serializer.data
        
        # Campos que deben estar presentes
        expected_fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'rol', 'puntos', 'contribuciones_aprobadas', 'date_joined'
        ]
        
        for field in expected_fields:
            self.assertIn(field, data)
    
    def test_serializer_read_only_fields(self):
        """Campos read-only no deben ser modificables"""
        from users.serializers import UserSerializer
        
        # Intentar modificar campos read-only
        data = {
            'username': 'newusername',
            'puntos': 999,  # read-only
            'contribuciones_aprobadas': 999  # read-only
        }
        
        serializer = UserSerializer(self.user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        
        updated_user = serializer.save()
        
        # Username debe cambiar
        self.assertEqual(updated_user.username, 'newusername')
        
        # Puntos y contribuciones NO deben cambiar
        self.assertEqual(updated_user.puntos, 100)
        self.assertEqual(updated_user.contribuciones_aprobadas, 5)
