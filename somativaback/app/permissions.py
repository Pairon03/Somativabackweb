from rest_framework import permissions
from .models.customuser import Cargo
from .models.customuser import Funcionario
from django.db.models import Q

def get_user_cargo(user):
    if user.is_superuser:
        return Cargo.ADMIN
    try:
        return user.cargo
    except:
        return None

class IsProducaoOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        cargo = get_user_cargo(request.user)
        return cargo in [Cargo.PRODUCAO, Cargo.ADMIN]

class IsEngenhariaOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        cargo = get_user_cargo(request.user)
        return cargo in [Cargo.ENGENHARIA, Cargo.ADMIN]

class IsManutencaoOrEngenhariaOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        cargo = get_user_cargo(request.user)
        return cargo in [Cargo.MANUTENCAO, Cargo.ENGENHARIA, Cargo.ADMIN]

class IsManutencaoOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        cargo = get_user_cargo(request.user)
        return cargo in [Cargo.MANUTENCAO, Cargo.ADMIN]
        
class IsLiderProducaoOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        cargo = get_user_cargo(request.user)
        return cargo in [Cargo.LIDER_PRODUCAO, Cargo.ADMIN]

class CategoriaPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        cargo = get_user_cargo(request.user)
        
        if cargo in [Cargo.ADMIN, Cargo.ENGENHARIA]:
            return True
            
        return request.method in permissions.SAFE_METHODS

class EngenhariaCanViewOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        cargo = get_user_cargo(request.user)
        
        if cargo in [Cargo.ADMIN, Cargo.PRODUCAO]:
            return True

        if cargo == Cargo.ENGENHARIA:
            return request.method in permissions.SAFE_METHODS
            
        return False