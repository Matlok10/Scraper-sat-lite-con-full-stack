from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo de Usuario personalizado.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'rol', 'puntos', 'contribuciones_aprobadas', 'date_joined')
        read_only_fields = ('id', 'date_joined', 'puntos', 'contribuciones_aprobadas')
