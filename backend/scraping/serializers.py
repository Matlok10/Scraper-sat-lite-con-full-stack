from rest_framework import serializers
from .models import Grupos, Tarea_Scrapeo, Sesion_Scraping, Post_Scrapeado

class GruposSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grupos
        fields = '__all__'

class TareaScrapeoSerializer(serializers.ModelSerializer):
    grupo_nombre = serializers.ReadOnlyField(source='grupo.nombre')
    
    class Meta:
        model = Tarea_Scrapeo
        fields = '__all__'

class SesionScrapingSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.ReadOnlyField(source='usuario.username')
    
    class Meta:
        model = Sesion_Scraping
        fields = '__all__'

class PostScrapeadoSerializer(serializers.ModelSerializer):
    grupo_nombre = serializers.ReadOnlyField(source='grupo.nombre')
    
    class Meta:
        model = Post_Scrapeado
        fields = '__all__'
