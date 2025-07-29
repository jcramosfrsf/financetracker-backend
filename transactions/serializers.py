from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .models import (
    Category, Transaction, CategoryAnalysis, SavingsGoal, 
    SavingsTransaction, AutoSaveRule, SavingsRecommendation, 
    SavingsInsight, SavingsAchievement, SavingsSimulation, SavingsReminder
)

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


# ============================================================================
# SERIALIZERS PARA EL SISTEMA DE AHORRO INTELIGENTE
# ============================================================================

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Fondo de emergencia',
            value={
                'id': 1,
                'user': 1,
                'name': 'Fondo de Emergencia',
                'description': 'Ahorrar 6 meses de gastos para emergencias',
                'goal_type': 'emergency_fund',
                'target_amount': '15000.00',
                'current_amount': '5000.00',
                'target_date': '2024-12-31',
                'priority': 'high',
                'status': 'active',
                'auto_save_percentage': 15.00,
                'auto_save_fixed_amount': 0.00,
                'auto_save_enabled': True,
                'progress_percentage': 33.33,
                'remaining_amount': 10000.00,
                'days_remaining': 180,
                'monthly_savings_needed': 555.56,
                'is_on_track': True,
                'risk_level': 'low',
                'created_at': '2024-01-01T00:00:00Z',
                'updated_at': '2024-01-15T10:30:00Z',
                'completed_at': None
            }
        ),
        OpenApiExample(
            'Vacaciones en Europa',
            value={
                'id': 2,
                'user': 1,
                'name': 'Vacaciones en Europa',
                'description': 'Ahorrar para un viaje de 3 semanas por Europa',
                'goal_type': 'vacation',
                'target_amount': '8000.00',
                'current_amount': '2000.00',
                'target_date': '2024-06-30',
                'priority': 'medium',
                'status': 'active',
                'auto_save_percentage': 10.00,
                'auto_save_fixed_amount': 200.00,
                'auto_save_enabled': True,
                'progress_percentage': 25.00,
                'remaining_amount': 6000.00,
                'days_remaining': 90,
                'monthly_savings_needed': 2000.00,
                'is_on_track': False,
                'risk_level': 'high',
                'created_at': '2024-01-01T00:00:00Z',
                'updated_at': '2024-01-15T10:30:00Z',
                'completed_at': None
            }
        )
    ]
)
class SavingsGoalSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SavingsGoal.
    
    Permite gestionar metas de ahorro inteligentes con configuración automática.
    """
    progress_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    remaining_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    monthly_savings_needed = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    is_on_track = serializers.BooleanField(read_only=True)
    risk_level = serializers.CharField(read_only=True)
    
    class Meta:
        model = SavingsGoal
        fields = [
            'id', 'user', 'name', 'description', 'goal_type', 'target_amount', 
            'current_amount', 'target_date', 'priority', 'status',
            'auto_save_percentage', 'auto_save_fixed_amount', 'auto_save_enabled',
            'progress_percentage', 'remaining_amount', 'days_remaining', 
            'monthly_savings_needed', 'is_on_track', 'risk_level',
            'created_at', 'updated_at', 'completed_at'
        ]
        read_only_fields = ['id', 'user', 'current_amount', 'progress_percentage', 
                           'remaining_amount', 'days_remaining', 'monthly_savings_needed',
                           'is_on_track', 'risk_level', 'created_at', 'updated_at', 'completed_at']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Depósito manual',
            value={
                'id': 1,
                'savings_goal': 1,
                'savings_goal_name': 'Fondo de Emergencia',
                'amount': '500.00',
                'transaction_type': 'deposit',
                'description': 'Depósito manual para meta de vacaciones',
                'date': '2024-01-15',
                'created_at': '2024-01-15T10:30:00Z'
            }
        ),
        OpenApiExample(
            'Ahorro automático',
            value={
                'id': 2,
                'savings_goal': 1,
                'savings_goal_name': 'Fondo de Emergencia',
                'amount': '150.00',
                'transaction_type': 'auto_save',
                'description': 'Ahorro automático: Porcentaje de Ingresos',
                'date': '2024-01-15',
                'created_at': '2024-01-15T10:30:00Z'
            }
        )
    ]
)
class SavingsTransactionSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SavingsTransaction.
    
    Permite gestionar transacciones específicas de ahorro para metas.
    """
    savings_goal_name = serializers.CharField(source='savings_goal.name', read_only=True)
    
    class Meta:
        model = SavingsTransaction
        fields = ['id', 'savings_goal', 'savings_goal_name', 'amount', 'transaction_type', 
                 'description', 'date', 'created_at']
        read_only_fields = ['id', 'savings_goal_name', 'created_at']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Regla de porcentaje de ingresos',
            value={
                'id': 1,
                'user': 1,
                'savings_goal': 1,
                'rule_type': 'percentage_income',
                'frequency': 'monthly',
                'percentage': 15.00,
                'fixed_amount': 0.00,
                'max_amount': 1000.00,
                'excess_threshold': 0.00,
                'excess_percentage': 50.00,
                'is_active': True,
                'last_executed': '2024-01-15T10:30:00Z',
                'next_execution': '2024-02-15T10:30:00Z',
                'created_at': '2024-01-01T00:00:00Z',
                'updated_at': '2024-01-15T10:30:00Z'
            }
        ),
        OpenApiExample(
            'Regla de cantidad fija',
            value={
                'id': 2,
                'user': 1,
                'savings_goal': 2,
                'rule_type': 'fixed_amount',
                'frequency': 'biweekly',
                'percentage': 0.00,
                'fixed_amount': 200.00,
                'max_amount': None,
                'excess_threshold': 0.00,
                'excess_percentage': 50.00,
                'is_active': True,
                'last_executed': '2024-01-01T10:30:00Z',
                'next_execution': '2024-01-15T10:30:00Z',
                'created_at': '2024-01-01T00:00:00Z',
                'updated_at': '2024-01-01T10:30:00Z'
            }
        )
    ]
)
class AutoSaveRuleSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo AutoSaveRule.
    
    Permite gestionar reglas de ahorro automático.
    """
    savings_goal_name = serializers.CharField(source='savings_goal.name', read_only=True)
    
    class Meta:
        model = AutoSaveRule
        fields = [
            'id', 'user', 'savings_goal', 'savings_goal_name', 'rule_type', 'frequency',
            'percentage', 'fixed_amount', 'max_amount', 'excess_threshold', 'excess_percentage',
            'is_active', 'last_executed', 'next_execution', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'savings_goal_name', 'last_executed', 'next_execution', 
                           'created_at', 'updated_at']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Recomendación de reducción de gastos',
            value={
                'id': 1,
                'user': 1,
                'savings_goal': 1,
                'savings_goal_name': 'Fondo de Emergencia',
                'recommendation_type': 'spending_reduction',
                'title': 'Reducir gastos en entretenimiento',
                'description': 'Has gastado 30% más en entretenimiento este mes. Considera reducir estos gastos para alcanzar tu meta de ahorro más rápido.',
                'priority': 'medium',
                'estimated_savings': 200.00,
                'implementation_difficulty': 'low',
                'time_to_implement': 1,
                'category_id': 3,
                'action_items': ['Cancelar suscripciones no utilizadas', 'Buscar alternativas gratuitas'],
                'is_read': False,
                'is_implemented': False,
                'implemented_at': None,
                'created_at': '2024-01-15T10:30:00Z',
                'updated_at': '2024-01-15T10:30:00Z'
            }
        ),
        OpenApiExample(
            'Recomendación de fondo de emergencia',
            value={
                'id': 2,
                'user': 1,
                'savings_goal': None,
                'savings_goal_name': None,
                'recommendation_type': 'emergency_fund',
                'title': 'Crear fondo de emergencia',
                'description': 'No tienes un fondo de emergencia. Se recomienda ahorrar al menos 3-6 meses de gastos para emergencias.',
                'priority': 'high',
                'estimated_savings': 0.00,
                'implementation_difficulty': 'medium',
                'time_to_implement': 30,
                'category_id': None,
                'action_items': ['Crear meta de ahorro para emergencias', 'Configurar ahorro automático'],
                'is_read': False,
                'is_implemented': False,
                'implemented_at': None,
                'created_at': '2024-01-15T10:30:00Z',
                'updated_at': '2024-01-15T10:30:00Z'
            }
        )
    ]
)
class SavingsRecommendationSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SavingsRecommendation.
    
    Permite gestionar recomendaciones inteligentes de ahorro.
    """
    savings_goal_name = serializers.CharField(source='savings_goal.name', read_only=True)
    
    class Meta:
        model = SavingsRecommendation
        fields = [
            'id', 'user', 'savings_goal', 'savings_goal_name', 'recommendation_type',
            'title', 'description', 'priority', 'estimated_savings', 
            'implementation_difficulty', 'time_to_implement', 'category_id', 'action_items',
            'is_read', 'is_implemented', 'implemented_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'savings_goal_name', 'is_read', 'is_implemented',
                           'implemented_at', 'created_at', 'updated_at']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Insight de patrón de gastos',
            value={
                'id': 1,
                'user': 1,
                'insight_type': 'spending_pattern',
                'title': 'Gastos en alimentación aumentaron 25%',
                'description': 'Tus gastos en alimentación han aumentado significativamente este mes comparado con el mes anterior.',
                'data': {
                    'current_month': 450.00,
                    'previous_month': 360.00,
                    'increase_percentage': 25.0,
                    'category': 'Alimentación'
                },
                'period_start': '2024-01-01',
                'period_end': '2024-01-31',
                'created_at': '2024-01-15T10:30:00Z',
                'is_archived': False
            }
        ),
        OpenApiExample(
            'Insight de tasa de ahorro',
            value={
                'id': 2,
                'user': 1,
                'insight_type': 'savings_rate',
                'title': 'Tasa de ahorro del 15% este mes',
                'description': 'Has ahorrado el 15% de tus ingresos este mes, lo cual es excelente para alcanzar tus metas.',
                'data': {
                    'savings_rate': 15.0,
                    'total_income': 2500.00,
                    'total_savings': 375.00,
                    'recommended_rate': 20.0
                },
                'period_start': '2024-01-01',
                'period_end': '2024-01-31',
                'created_at': '2024-01-15T10:30:00Z',
                'is_archived': False
            }
        )
    ]
)
class SavingsInsightSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SavingsInsight.
    
    Permite gestionar insights y análisis de ahorro.
    """
    class Meta:
        model = SavingsInsight
        fields = [
            'id', 'user', 'insight_type', 'title', 'description', 'data',
            'period_start', 'period_end', 'created_at', 'is_archived'
        ]
        read_only_fields = ['id', 'user', 'created_at']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Logro de meta completada',
            value={
                'id': 1,
                'user': 1,
                'achievement_type': 'goal_completed',
                'title': '¡Meta completada: Fondo de Emergencia!',
                'description': 'Has alcanzado tu meta de ahorro de $15000',
                'points': 100,
                'data': {
                    'goal_name': 'Fondo de Emergencia',
                    'target_amount': 15000.00,
                    'completion_date': '2024-01-15'
                },
                'created_at': '2024-01-15T10:30:00Z'
            }
        ),
        OpenApiExample(
            'Logro de racha de ahorro',
            value={
                'id': 2,
                'user': 1,
                'achievement_type': 'savings_streak',
                'title': '¡Racha de 30 días de ahorro!',
                'description': 'Has ahorrado consecutivamente durante 30 días',
                'points': 50,
                'data': {
                    'streak_days': 30,
                    'total_saved': 1500.00
                },
                'created_at': '2024-01-15T10:30:00Z'
            }
        )
    ]
)
class SavingsAchievementSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SavingsAchievement.
    
    Permite gestionar logros y sistema de gamificación.
    """
    class Meta:
        model = SavingsAchievement
        fields = [
            'id', 'user', 'achievement_type', 'title', 'description', 'points', 'data', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Simulación de reducción de gastos',
            value={
                'id': 1,
                'user': 1,
                'simulation_type': 'spending_reduction',
                'title': '¿Qué pasaría si reduzco gastos en entretenimiento?',
                'description': 'Simulación de ahorro al reducir gastos en entretenimiento en un 20%',
                'parameters': {
                    'category_id': 3,
                    'reduction_percentage': 20,
                    'months': 3
                },
                'results': {
                    'total_savings': 180.00,
                    'monthly_savings': 60.00,
                    'goal_impact': {
                        'goal_id': 1,
                        'days_earlier': 15,
                        'new_completion_date': '2024-11-15'
                    }
                },
                'created_at': '2024-01-15T10:30:00Z',
                'is_saved': False
            }
        )
    ]
)
class SavingsSimulationSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SavingsSimulation.
    
    Permite gestionar simulaciones de ahorro.
    """
    class Meta:
        model = SavingsSimulation
        fields = [
            'id', 'user', 'simulation_type', 'title', 'description', 'parameters',
            'results', 'created_at', 'is_saved'
        ]
        read_only_fields = ['id', 'user', 'created_at']


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Recordatorio de ahorro pendiente',
            value={
                'id': 1,
                'user': 1,
                'reminder_type': 'savings_due',
                'title': 'Ahorro pendiente para esta semana',
                'message': 'Te falta ahorrar $200 para mantener el ritmo de tu meta de vacaciones',
                'priority': 'medium',
                'scheduled_for': '2024-01-20T09:00:00Z',
                'is_recurring': True,
                'recurrence_pattern': {
                    'frequency': 'weekly',
                    'day_of_week': 1
                },
                'is_sent': False,
                'sent_at': None,
                'is_dismissed': False,
                'dismissed_at': None,
                'related_goal_id': 2,
                'related_transaction_id': None,
                'created_at': '2024-01-15T10:30:00Z',
                'updated_at': '2024-01-15T10:30:00Z'
            }
        )
    ]
)
class SavingsReminderSerializer(serializers.ModelSerializer):
    """
    Serializer para el modelo SavingsReminder.
    
    Permite gestionar recordatorios inteligentes.
    """
    class Meta:
        model = SavingsReminder
        fields = [
            'id', 'user', 'reminder_type', 'title', 'message', 'priority',
            'scheduled_for', 'is_recurring', 'recurrence_pattern', 'is_sent', 'sent_at',
            'is_dismissed', 'dismissed_at', 'related_goal_id', 'related_transaction_id',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'is_sent', 'sent_at', 'is_dismissed', 'dismissed_at',
                           'created_at', 'updated_at']


# ============================================================================
# SERIALIZERS ADICIONALES PARA RESPUESTAS ESPECÍFICAS
# ============================================================================

class SavingsGoalProgressSerializer(serializers.Serializer):
    """
    Serializer para mostrar el progreso detallado de una meta de ahorro.
    """
    goal = SavingsGoalSerializer()
    recent_transactions = SavingsTransactionSerializer(many=True)
    monthly_progress = serializers.ListField(
        child=serializers.DictField(),
        help_text='Progreso mensual con fecha y cantidad'
    )
    projected_completion = serializers.DateField(allow_null=True)
    risk_level = serializers.CharField(help_text='low, medium, high, critical')


class SavingsDashboardSerializer(serializers.Serializer):
    """
    Serializer para el dashboard de ahorro.
    """
    total_savings = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_goals = serializers.IntegerField()
    active_goals = serializers.IntegerField()
    completed_goals = serializers.IntegerField()
    monthly_savings_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    goals_progress = serializers.ListField(
        child=SavingsGoalSerializer()
    )
    recent_recommendations = serializers.ListField(
        child=SavingsRecommendationSerializer()
    )
    insights = serializers.ListField(
        child=SavingsInsightSerializer()
    )
    achievements = serializers.ListField(
        child=SavingsAchievementSerializer()
    )
    pending_reminders = serializers.ListField(
        child=SavingsReminderSerializer()
    )


class AutoSaveConfigSerializer(serializers.Serializer):
    """
    Serializer para configuración de ahorro automático.
    """
    enabled = serializers.BooleanField()
    percentage_of_income = serializers.DecimalField(max_digits=5, decimal_places=2)
    fixed_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    frequency = serializers.CharField(help_text='weekly, biweekly, monthly')
    next_auto_save_date = serializers.DateField()
    total_auto_saved = serializers.DecimalField(max_digits=12, decimal_places=2)


class SavingsSimulationRequestSerializer(serializers.Serializer):
    """
    Serializer para solicitudes de simulación.
    """
    simulation_type = serializers.ChoiceField(choices=SavingsSimulation.SIMULATION_TYPE_CHOICES)
    parameters = serializers.DictField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField()


class SavingsRecommendationRequestSerializer(serializers.Serializer):
    """
    Serializer para solicitudes de recomendaciones.
    """
    goal_id = serializers.IntegerField(required=False, allow_null=True)
    category_id = serializers.IntegerField(required=False, allow_null=True)
    include_implemented = serializers.BooleanField(default=False) 