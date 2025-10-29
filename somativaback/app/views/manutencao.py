from .__init__ import *
from ..models.manutencao import Manutencao
from ..serializers.manutencao import ManutencaoSerializer

class ManutencaoViewSet(viewsets.ModelViewSet):
    queryset = Manutencao.objects.all()
    serializer_class = ManutencaoSerializer
    permission_classes = [IsManutencaoOrEngenhariaOrAdmin]