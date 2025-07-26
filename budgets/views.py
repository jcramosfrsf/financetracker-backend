from django.shortcuts import render
from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import Budget
from .serializers import BudgetSerializer
from transactions.views import IsOwner

# Create your views here.

@extend_schema_view(
    list=extend_schema(
        summary="Listar presupuestos",
        description="Obtiene todos los presupuestos del usuario autenticado",
        parameters=[
            OpenApiParameter(
                name='category',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filtrar por ID de categoría'
            ),
            OpenApiParameter(
                name='active',
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description='Filtrar presupuestos activos (fecha actual entre start_date y end_date)'
            ),
        ],
        tags=['budgets']
    ),
    create=extend_schema(
        summary="Crear presupuesto",
        description="Crea un nuevo presupuesto para una categoría específica",
        examples=[
            OpenApiExample(
                'Presupuesto mensual',
                value={
                    'category': 1,
                    'amount': '500.00',
                    'start_date': '2024-01-01',
                    'end_date': '2024-01-31'
                }
            ),
        ],
        tags=['budgets']
    ),
    retrieve=extend_schema(
        summary="Obtener presupuesto",
        description="Obtiene los detalles de un presupuesto específico",
        tags=['budgets']
    ),
    update=extend_schema(
        summary="Actualizar presupuesto",
        description="Actualiza completamente un presupuesto existente",
        tags=['budgets']
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente presupuesto",
        description="Actualiza parcialmente un presupuesto existente",
        tags=['budgets']
    ),
    destroy=extend_schema(
        summary="Eliminar presupuesto",
        description="Elimina un presupuesto existente",
        tags=['budgets']
    ),
)
class BudgetViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar presupuestos financieros.
    
    Permite crear, leer, actualizar y eliminar presupuestos por categoría
    con fechas de inicio y fin específicas.
    """
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        queryset = self.request.user.budgets.all()
        
        # Filtros opcionales
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
            
        active = self.request.query_params.get('active', None)
        if active is not None:
            from django.utils import timezone
            today = timezone.now().date()
            if active.lower() == 'true':
                queryset = queryset.filter(start_date__lte=today, end_date__gte=today)
            elif active.lower() == 'false':
                queryset = queryset.exclude(start_date__lte=today, end_date__gte=today)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
