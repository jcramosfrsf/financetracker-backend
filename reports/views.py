from django.shortcuts import render
from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import Report
from .serializers import ReportSerializer
from transactions.views import IsOwner

# Create your views here.

@extend_schema_view(
    list=extend_schema(
        summary="Listar reportes",
        description="Obtiene todos los reportes del usuario autenticado",
        parameters=[
            OpenApiParameter(
                name='report_type',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filtrar por tipo de reporte',
                examples=[
                    OpenApiExample('Resumen mensual', value='monthly_summary'),
                    OpenApiExample('Gastos por categoría', value='spending_by_category'),
                ]
            ),
            OpenApiParameter(
                name='start_date',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Filtrar reportes desde esta fecha (YYYY-MM-DD)'
            ),
            OpenApiParameter(
                name='end_date',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Filtrar reportes hasta esta fecha (YYYY-MM-DD)'
            ),
        ],
        tags=['reports']
    ),
    create=extend_schema(
        summary="Crear reporte",
        description="Crea un nuevo reporte financiero",
        examples=[
            OpenApiExample(
                'Resumen mensual',
                value={
                    'name': 'Resumen Enero 2024',
                    'report_type': 'monthly_summary',
                    'start_date': '2024-01-01',
                    'end_date': '2024-01-31',
                    'data': {}
                }
            ),
            OpenApiExample(
                'Gastos por categoría',
                value={
                    'name': 'Análisis de gastos Q1 2024',
                    'report_type': 'spending_by_category',
                    'start_date': '2024-01-01',
                    'end_date': '2024-03-31',
                    'data': {}
                }
            ),
        ],
        tags=['reports']
    ),
    retrieve=extend_schema(
        summary="Obtener reporte",
        description="Obtiene los detalles de un reporte específico",
        tags=['reports']
    ),
    update=extend_schema(
        summary="Actualizar reporte",
        description="Actualiza completamente un reporte existente",
        tags=['reports']
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente reporte",
        description="Actualiza parcialmente un reporte existente",
        tags=['reports']
    ),
    destroy=extend_schema(
        summary="Eliminar reporte",
        description="Elimina un reporte existente",
        tags=['reports']
    ),
)
class ReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar reportes financieros.
    
    Permite crear, leer, actualizar y eliminar reportes financieros
    con diferentes tipos de análisis y rangos de fechas.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        queryset = self.request.user.reports.all()
        
        # Filtros opcionales
        report_type = self.request.query_params.get('report_type', None)
        if report_type:
            queryset = queryset.filter(report_type=report_type)
            
        start_date = self.request.query_params.get('start_date', None)
        if start_date:
            queryset = queryset.filter(start_date__gte=start_date)
            
        end_date = self.request.query_params.get('end_date', None)
        if end_date:
            queryset = queryset.filter(end_date__lte=end_date)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
