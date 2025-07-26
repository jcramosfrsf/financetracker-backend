from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .models import Category, Transaction, CategoryAnalysis

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Categoría de ejemplo',
            value={
                'id': 1,
                'name': 'Alimentación',
                'user': 1,
                'color': '#3B82F6',
                'icon': 'shopping-cart'
            }
        )
    ]
)
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Category.
    
    Permite serializar y deserializar categorías de transacciones.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'user', 'color', 'icon']
        read_only_fields = ['id', 'user']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Transacción de ingreso',
            value={
                'id': 1,
                'user': 1,
                'category': 1,
                'transaction_type': 'income',
                'amount': '1500.00',
                'date': '2024-01-15',
                'description': 'Salario mensual',
                'created_at': '2024-01-15T10:30:00Z',
                'updated_at': '2024-01-15T10:30:00Z'
            }
        ),
        OpenApiExample(
            'Transacción de gasto',
            value={
                'id': 2,
                'user': 1,
                'category': 2,
                'transaction_type': 'expense',
                'amount': '50.00',
                'date': '2024-01-15',
                'description': 'Compra de comestibles',
                'created_at': '2024-01-15T14:20:00Z',
                'updated_at': '2024-01-15T14:20:00Z'
            }
        )
    ]
)
class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo Transaction.
    
    Permite serializar y deserializar transacciones financieras (ingresos y gastos).
    """
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'category', 'transaction_type', 'amount', 'date', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class CategoryAnalysisSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo CategoryAnalysis.
    
    Permite serializar análisis precalculados de categorías.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_color = serializers.CharField(source='category.color', read_only=True)
    
    class Meta:
        model = CategoryAnalysis
        fields = [
            'id', 'user', 'category', 'category_name', 'category_color',
            'period', 'start_date', 'end_date', 'total_income', 'total_expenses',
            'transaction_count', 'average_amount', 'percentage_of_total',
            'top_transactions', 'trend_data', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class CategorySummarySerializer(serializers.Serializer):
    """
    Serializer para resúmenes de categorías con métricas calculadas.
    """
    category_id = serializers.IntegerField()
    category_name = serializers.CharField()
    category_color = serializers.CharField()
    category_icon = serializers.CharField()
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    transaction_count = serializers.IntegerField()
    average_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    percentage_of_total_expenses = serializers.DecimalField(max_digits=5, decimal_places=2)
    percentage_of_total_income = serializers.DecimalField(max_digits=5, decimal_places=2)
    last_transaction_date = serializers.DateField(allow_null=True)
    trend = serializers.CharField(help_text='up, down, stable')


class CategoryTrendSerializer(serializers.Serializer):
    """
    Serializer para datos de tendencias de categorías.
    """
    category_id = serializers.IntegerField()
    category_name = serializers.CharField()
    period = serializers.CharField()
    data_points = serializers.ListField(
        child=serializers.DictField(),
        help_text='Lista de puntos de datos con fecha y valor'
    )
    trend_direction = serializers.CharField(help_text='up, down, stable')
    trend_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)


class CategoryComparisonSerializer(serializers.Serializer):
    """
    Serializer para comparaciones entre categorías.
    """
    period = serializers.CharField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    categories = serializers.ListField(
        child=CategorySummarySerializer()
    )
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    net_savings = serializers.DecimalField(max_digits=12, decimal_places=2) 