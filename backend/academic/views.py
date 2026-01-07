from rest_framework import viewsets
from .models import Catedra
from .serializers import CatedraSerializer

class CatedraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para visualizar y editar cátedras.
    """
    queryset = Catedra.objects.all()
    serializer_class = CatedraSerializer
