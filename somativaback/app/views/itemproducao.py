from .__init__ import *
from ..models.itemproducao import ItemProducao
from ..serializers.itemproducao import ItemProducaoSerializer

class ItemProducaoViewSet(viewsets.ModelViewSet):
    queryset = ItemProducao.objects.all()
    serializer_class = ItemProducaoSerializer
    permission_classes = [EngenhariaCanViewOnly]