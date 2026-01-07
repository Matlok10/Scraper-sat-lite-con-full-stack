from rest_framework import viewsets
from .models import Grupos, Tarea_Scrapeo, Sesion_Scraping, Post_Scrapeado
from .serializers import (
    GruposSerializer, TareaScrapeoSerializer, 
    SesionScrapingSerializer, PostScrapeadoSerializer
)

class GruposViewSet(viewsets.ModelViewSet):
    queryset = Grupos.objects.all()
    serializer_class = GruposSerializer

class TareaScrapeoViewSet(viewsets.ModelViewSet):
    queryset = Tarea_Scrapeo.objects.all()
    serializer_class = TareaScrapeoSerializer

class SesionScrapingViewSet(viewsets.ModelViewSet):
    queryset = Sesion_Scraping.objects.all()
    serializer_class = SesionScrapingSerializer

class PostScrapeadoViewSet(viewsets.ModelViewSet):
    queryset = Post_Scrapeado.objects.all()
    serializer_class = PostScrapeadoSerializer
