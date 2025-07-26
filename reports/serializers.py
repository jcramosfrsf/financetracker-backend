from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .models import Report

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Reporte de resumen mensual',
            value={
                'id': 1,
                'user': 1,
                'name': 'Resumen Enero 2024',
                'report_type': 'monthly_summary',
                'start_date': '2024-01-01',
                'end_date': '2024-01-31',
                'generated_at': '2024-01-31T23:59:59Z',
                'data': {
                    'total_income': 2500.00,
                    'total_expenses': 1800.00,
                    'net_savings': 700.00,
                    'top_categories': [
                        {'category': 'Alimentación', 'amount': 400.00},
                        {'category': 'Transporte', 'amount': 300.00}
                    ]
                }
            }
        ),
        OpenApiExample(
            'Reporte de gastos por categoría',
            value={
                'id': 2,
                'user': 1,
                'name': 'Análisis de gastos Q1 2024',
                'report_type': 'spending_by_category',
                'start_date': '2024-01-01',
                'end_date': '2024-03-31',
                'generated_at': '2024-04-01T00:00:00Z',
                'data': {
                    'categories': [
                        {'name': 'Alimentación', 'total': 1200.00, 'percentage': 30},
                        {'name': 'Transporte', 'total': 900.00, 'percentage': 22.5},
                        {'name': 'Entretenimiento', 'total': 600.00, 'percentage': 15}
                    ],
                    'total_expenses': 4000.00
                }
            }
        )
    ]
)
class ReportSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Report.
    
    Permite serializar y deserializar reportes financieros con datos JSON.
    """
    class Meta:
        model = Report
        fields = ['id', 'user', 'name', 'report_type', 'start_date', 'end_date', 'generated_at', 'data']
        read_only_fields = ['id', 'user', 'generated_at'] 