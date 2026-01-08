from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User
from .serializers import UserSerializer

class UserLoginView(ObtainAuthToken):
    """
    Vista para autenticación de usuarios y obtención de token.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            'rol': user.rol
        })

class UserLogoutView(APIView):
    """
    Vista para cerrar sesión y eliminar el token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de usuarios.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        Permite list/update/delete/assign_role solo a admins.
        Cualquier autenticado puede ver su perfil ('me') o retrieve.
        """
        if self.action in ['list', 'destroy', 'update', 'partial_update', 'assign_role']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Endpoint para obtener datos del usuario actual."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def assign_role(self, request, pk=None):
        """Asignar rol a un usuario (Solo Admin)."""
        user = self.get_object()
        rol = request.data.get('rol')
        
        # Validar rol
        valid_roles = dict(User.ROL_CHOICES).keys()
        if rol not in valid_roles:
            return Response(
                {'error': f'Rol inválido. Opciones: {list(valid_roles)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user.rol = rol
        user.save()
        return Response({'status': f'Rol actualizado a {rol}'})
