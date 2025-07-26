from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .models import Budget

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Presupuesto de ejemplo',
            value={
                'id': 1,
                'user': 1,
                'category': 1,
                'amount': '500.00',
                'start_date': '2024-01-01',
                'end_date': '2024-01-31'
            }
        )
    ]
)
class BudgetSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Budget.
    
    Permite serializar y deserializar presupuestos financieros por categoría.
    """
    class Meta:
        model = Budget
        fields = ['id', 'user', 'category', 'amount', 'start_date', 'end_date']
        read_only_fields = ['id', 'user'] 