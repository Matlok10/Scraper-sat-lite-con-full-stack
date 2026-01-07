from rest_framework import serializers
from .models import Catedra

class CatedraSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo de Cátedra.
    """
    class Meta:
        model = Catedra
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'ultima_actualizacion_scraping')
