from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
# from django_filters.rest_framework import DjangoFilterBackend 
from django.utils import timezone
from datetime import timedelta

from ..models.customuser import Funcionario, Cargo

from ..permissions import (
    IsProducaoOrAdmin, IsEngenhariaOrAdmin, IsManutencaoOrEngenhariaOrAdmin, 
    CategoriaPermission, EngenhariaCanViewOnly, IsManutencaoOrAdmin, IsLiderProducaoOrAdmin,
    get_user_cargo 
)


class ReadWriteSerializerMixin(object):
    read_serializer_class = None
    write_serializer_class = None

    def get_read_serializer_class(self):
        return self.read_serializer_class
    
    def get_write_serializer_class(self):
        return self.write_serializer_class
    
    def get_serializer_class(self):
        if self.action in ['create','update', 'partial_update','destroy']:
            return self.get_write_serializer_class()
        return self.get_read_serializer_class()