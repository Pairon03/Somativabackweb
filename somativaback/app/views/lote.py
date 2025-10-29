from .__init__ import *
from ..models.lote import Lote
from ..models.itemproducao import ItemProducao 
from ..serializers.lote import LoteDetailSerializer, LoteSerializer


class LoteViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    read_serializer_class = LoteDetailSerializer
    write_serializer_class = LoteSerializer
    
    def get_queryset(self):
        user = self.request.user
        cargo = get_user_cargo(user)
        queryset = Lote.objects.all().select_related('responsavel_inspecao')
        
        if cargo == Cargo.INSPECAO:
            queryset = queryset.filter(
                Q(status_inspecao='PENDENTE') | Q(responsavel_inspecao=user)
            )
            
        if cargo in [Cargo.ENGENHARIA, Cargo.ADMIN, Cargo.PRODUCAO, Cargo.LIDER_PRODUCAO]:
            return queryset
            
        return queryset.none() if not user.is_authenticated else queryset

    @action(detail=False, methods=['get'], permission_classes=[IsLiderProducaoOrAdmin])
    def dashboard(self, request):
        
        queryset = ItemProducao.objects.all().select_related('lote')
        
        aprovados = queryset.filter(lote__status_inspecao='APROVADO').count()
        reprovados = queryset.filter(lote__status_inspecao='REPROVADO').count()
        pendentes = queryset.filter(lote__status_inspecao='PENDENTE').count()
        
        data = {
            'total_pecas_aprovadas': aprovados,
            'total_pecas_reprovadas': reprovados,
            'total_pecas_pendentes_inspecao': pendentes,
            'total_pecas_produzidas': aprovados + reprovados + pendentes
        }

        return Response(data)