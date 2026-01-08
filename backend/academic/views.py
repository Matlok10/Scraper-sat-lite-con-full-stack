from rest_framework import viewsets
from .models import Comision
from .serializers import ComisionSerializer

class ComisionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar y editar comisiones.
    """
    queryset = Comision.objects.all()
    serializer_class = ComisionSerializer
