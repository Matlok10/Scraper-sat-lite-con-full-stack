from rest_framework import serializers
from .models import Comision

class ComisionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo de Comisión.
    """
    class Meta:
        model = Comision
        fields = '__all__'
        read_only_fields = ('fecha_creacion', 'ultima_actualizacion_scraping')
