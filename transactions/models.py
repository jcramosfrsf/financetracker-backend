from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
import json


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#3B82F6', help_text='Color hexadecimal para la categoría')
    icon = models.CharField(max_length=50, blank=True, help_text='Nombre del icono (ej: shopping-cart, food, etc.)')

    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name

    def get_total_amount(self, transaction_type=None, start_date=None, end_date=None):
        """Obtiene el total de transacciones para esta categoría en un período específico"""
        queryset = self.transactions.all()
        
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
            
        return queryset.aggregate(total=Sum('amount'))['total'] or 0

    def get_transaction_count(self, transaction_type=None, start_date=None, end_date=None):
        """Obtiene el número de transacciones para esta categoría en un período específico"""
        queryset = self.transactions.all()
        
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
            
        return queryset.count()

    def get_average_amount(self, transaction_type=None, start_date=None, end_date=None):
        """Obtiene el promedio de transacciones para esta categoría en un período específico"""
        queryset = self.transactions.all()
        
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
            
        return queryset.aggregate(average=Avg('amount'))['average'] or 0


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    transaction_type = models.CharField(max_length=7, choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.description} - {self.amount}'


class CategoryAnalysis(models.Model):
    """Modelo para almacenar análisis precalculados por categoría"""
    ANALYSIS_PERIOD_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_analyses')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='analyses')
    period = models.CharField(max_length=10, choices=ANALYSIS_PERIOD_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Métricas calculadas
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    transaction_count = models.IntegerField(default=0)
    average_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    percentage_of_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Datos adicionales
    top_transactions = models.JSONField(default=list, blank=True)
    trend_data = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'category', 'period', 'start_date', 'end_date']
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.category.name} - {self.period} ({self.start_date} to {self.end_date})'

    @classmethod
    def generate_analysis(cls, user, category, period, start_date, end_date):
        """Genera un análisis para una categoría específica en un período dado"""
        # Obtener transacciones del período
        transactions = Transaction.objects.filter(
            user=user,
            category=category,
            date__range=[start_date, end_date]
        )
        
        # Calcular métricas
        total_income = transactions.filter(transaction_type='income').aggregate(
            total=Sum('amount'))['total'] or 0
        total_expenses = transactions.filter(transaction_type='expense').aggregate(
            total=Sum('amount'))['total'] or 0
        transaction_count = transactions.count()
        average_amount = transactions.aggregate(avg=Avg('amount'))['avg'] or 0
        
        # Calcular porcentaje del total (solo para gastos)
        if total_expenses > 0:
            total_user_expenses = Transaction.objects.filter(
                user=user,
                transaction_type='expense',
                date__range=[start_date, end_date]
            ).aggregate(total=Sum('amount'))['total'] or 0
            percentage_of_total = (total_expenses / total_user_expenses * 100) if total_user_expenses > 0 else 0
        else:
            percentage_of_total = 0
        
        # Obtener transacciones más importantes
        top_transactions = list(transactions.order_by('-amount')[:5].values(
            'id', 'amount', 'transaction_type', 'date', 'description'
        ))
        
        # Crear o actualizar el análisis
        analysis, created = cls.objects.update_or_create(
            user=user,
            category=category,
            period=period,
            start_date=start_date,
            end_date=end_date,
            defaults={
                'total_income': total_income,
                'total_expenses': total_expenses,
                'transaction_count': transaction_count,
                'average_amount': average_amount,
                'percentage_of_total': percentage_of_total,
                'top_transactions': top_transactions,
            }
        )
        
        return analysis


# ============================================================================
# SISTEMA DE AHORRO INTELIGENTE
# ============================================================================

class SavingsGoal(models.Model):
    """Modelo para metas de ahorro inteligentes"""
    GOAL_TYPE_CHOICES = (
        ('emergency_fund', 'Fondo de Emergencia'),
        ('vacation', 'Vacaciones'),
        ('house', 'Casa'),
        ('car', 'Auto'),
        ('education', 'Educación'),
        ('retirement', 'Jubilación'),
        ('wedding', 'Boda'),
        ('business', 'Negocio'),
        ('custom', 'Personalizado'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('critical', 'Crítica'),
    )
    
    STATUS_CHOICES = (
        ('active', 'Activa'),
        ('paused', 'Pausada'),
        ('completed', 'Completada'),
        ('cancelled', 'Cancelada'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_goals')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    target_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    # Configuración de ahorro automático
    auto_save_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.00, 
                                             help_text='Porcentaje de ingresos a ahorrar automáticamente')
    auto_save_fixed_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                               help_text='Cantidad fija a ahorrar automáticamente')
    auto_save_enabled = models.BooleanField(default=True)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return f'{self.name} - {self.user.username}'

    @property
    def progress_percentage(self):
        """Calcula el porcentaje de progreso hacia la meta"""
        if self.target_amount <= 0:
            return 0
        return min((self.current_amount / self.target_amount) * 100, 100)

    @property
    def remaining_amount(self):
        """Calcula la cantidad restante para alcanzar la meta"""
        return max(self.target_amount - self.current_amount, 0)

    @property
    def days_remaining(self):
        """Calcula los días restantes hasta la fecha objetivo"""
        today = timezone.now().date()
        if self.target_date <= today:
            return 0
        return (self.target_date - today).days

    @property
    def monthly_savings_needed(self):
        """Calcula cuánto necesita ahorrar por mes para alcanzar la meta"""
        if self.days_remaining <= 0:
            return self.remaining_amount
        
        months_remaining = self.days_remaining / 30.44  # Promedio de días por mes
        if months_remaining <= 0:
            return self.remaining_amount
        
        return self.remaining_amount / months_remaining

    @property
    def is_on_track(self):
        """Determina si la meta está en camino de ser alcanzada a tiempo"""
        if self.days_remaining <= 0:
            return self.progress_percentage >= 100
        
        # Calcular la tasa de ahorro necesaria
        needed_rate = self.remaining_amount / self.days_remaining
        
        # Calcular la tasa actual de ahorro (últimos 30 días)
        thirty_days_ago = timezone.now().date() - timedelta(days=30)
        recent_savings = self.savings_transactions.filter(
            date__gte=thirty_days_ago,
            transaction_type='deposit'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        current_rate = recent_savings / 30  # por día
        
        return current_rate >= needed_rate

    @property
    def risk_level(self):
        """Determina el nivel de riesgo de no alcanzar la meta"""
        if self.progress_percentage >= 100:
            return 'completed'
        elif self.days_remaining <= 30 and self.progress_percentage < 80:
            return 'critical'
        elif self.days_remaining <= 90 and self.progress_percentage < 60:
            return 'high'
        elif not self.is_on_track:
            return 'medium'
        else:
            return 'low'

    def add_savings(self, amount, description="", date=None, transaction_type='deposit'):
        """Agrega una cantidad a los ahorros de esta meta"""
        if date is None:
            date = timezone.now().date()
        
        # Crear transacción de ahorro
        savings_transaction = SavingsTransaction.objects.create(
            savings_goal=self,
            amount=amount,
            description=description,
            date=date,
            transaction_type=transaction_type
        )
        
        # Actualizar cantidad actual
        if transaction_type == 'deposit':
            self.current_amount += amount
        elif transaction_type == 'withdrawal':
            self.current_amount = max(0, self.current_amount - amount)
        
        self.save()
        
        # Verificar si la meta se completó
        if self.current_amount >= self.target_amount and self.status == 'active':
            self.status = 'completed'
            self.completed_at = timezone.now()
            self.save()
            
            # Crear logro por completar meta
            SavingsAchievement.objects.create(
                user=self.user,
                achievement_type='goal_completed',
                title=f'¡Meta completada: {self.name}!',
                description=f'Has alcanzado tu meta de ahorro de ${self.target_amount}',
                points=100
            )
        
        return savings_transaction


class SavingsTransaction(models.Model):
    """Modelo para transacciones de ahorro específicas de metas"""
    TRANSACTION_TYPE_CHOICES = (
        ('deposit', 'Depósito'),
        ('withdrawal', 'Retiro'),
        ('adjustment', 'Ajuste'),
        ('auto_save', 'Ahorro Automático'),
        ('excess_savings', 'Ahorro por Excedente'),
    )

    savings_goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE, related_name='savings_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPE_CHOICES, default='deposit')
    description = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.savings_goal.name} - {self.amount} ({self.date})'


class AutoSaveRule(models.Model):
    """Modelo para reglas de ahorro automático"""
    RULE_TYPE_CHOICES = (
        ('percentage_income', 'Porcentaje de Ingresos'),
        ('fixed_amount', 'Cantidad Fija'),
        ('excess_budget', 'Excedente de Presupuesto'),
        ('round_up', 'Redondeo'),
        ('smart_savings', 'Ahorro Inteligente'),
    )
    
    FREQUENCY_CHOICES = (
        ('daily', 'Diario'),
        ('weekly', 'Semanal'),
        ('biweekly', 'Quincenal'),
        ('monthly', 'Mensual'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auto_save_rules')
    savings_goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE, related_name='auto_save_rules')
    rule_type = models.CharField(max_length=20, choices=RULE_TYPE_CHOICES)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES, default='monthly')
    
    # Configuración específica por tipo de regla
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.00, 
                                   help_text='Porcentaje para reglas de tipo percentage_income')
    fixed_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                     help_text='Cantidad fija para reglas de tipo fixed_amount')
    max_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
                                   help_text='Monto máximo para ahorro automático')
    
    # Configuración de excedentes
    excess_threshold = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                         help_text='Umbral mínimo para considerar excedente')
    excess_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=50.00,
                                          help_text='Porcentaje del excedente a ahorrar')
    
    # Estado
    is_active = models.BooleanField(default=True)
    last_executed = models.DateTimeField(null=True, blank=True)
    next_execution = models.DateTimeField(null=True, blank=True)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.rule_type} - {self.savings_goal.name}'

    def calculate_savings_amount(self, income_amount=0, budget_excess=0):
        """Calcula la cantidad a ahorrar según el tipo de regla"""
        if self.rule_type == 'percentage_income':
            amount = (income_amount * self.percentage) / 100
        elif self.rule_type == 'fixed_amount':
            amount = self.fixed_amount
        elif self.rule_type == 'excess_budget':
            if budget_excess > self.excess_threshold:
                amount = (budget_excess * self.excess_percentage) / 100
            else:
                amount = 0
        elif self.rule_type == 'round_up':
            # Redondear al siguiente múltiplo de 10
            amount = ((income_amount // 10) + 1) * 10 - income_amount
        elif self.rule_type == 'smart_savings':
            # Ahorro inteligente basado en análisis de gastos
            amount = self._calculate_smart_savings(income_amount)
        else:
            amount = 0
        
        # Aplicar límite máximo si existe
        if self.max_amount and amount > self.max_amount:
            amount = self.max_amount
        
        return max(0, amount)

    def _calculate_smart_savings(self, income_amount):
        """Calcula ahorro inteligente basado en patrones de gastos"""
        # Obtener gastos promedio de los últimos 3 meses
        three_months_ago = timezone.now().date() - timedelta(days=90)
        avg_expenses = Transaction.objects.filter(
            user=self.user,
            transaction_type='expense',
            date__gte=three_months_ago
        ).aggregate(avg=Avg('amount'))['avg'] or 0
        
        # Calcular ahorro sugerido (20% del ingreso o excedente)
        suggested_savings = income_amount * 0.2
        
        # Si los gastos promedio son altos, sugerir más ahorro
        if avg_expenses > income_amount * 0.7:
            suggested_savings = income_amount * 0.3
        
        return suggested_savings

    def execute(self, income_amount=0, budget_excess=0):
        """Ejecuta la regla de ahorro automático"""
        if not self.is_active:
            return None
        
        amount = self.calculate_savings_amount(income_amount, budget_excess)
        
        if amount > 0:
            # Crear transacción de ahorro
            transaction = self.savings_goal.add_savings(
                amount=amount,
                description=f'Ahorro automático: {self.get_rule_type_display()}',
                transaction_type='auto_save'
            )
            
            # Actualizar fechas de ejecución
            self.last_executed = timezone.now()
            self._calculate_next_execution()
            self.save()
            
            return transaction
        
        return None

    def _calculate_next_execution(self):
        """Calcula la próxima fecha de ejecución"""
        if self.frequency == 'daily':
            self.next_execution = timezone.now() + timedelta(days=1)
        elif self.frequency == 'weekly':
            self.next_execution = timezone.now() + timedelta(weeks=1)
        elif self.frequency == 'biweekly':
            self.next_execution = timezone.now() + timedelta(weeks=2)
        elif self.frequency == 'monthly':
            self.next_execution = timezone.now() + timedelta(days=30)


class SavingsRecommendation(models.Model):
    """Modelo para recomendaciones de ahorro inteligentes"""
    RECOMMENDATION_TYPE_CHOICES = (
        ('spending_reduction', 'Reducción de Gastos'),
        ('income_increase', 'Aumento de Ingresos'),
        ('goal_adjustment', 'Ajuste de Meta'),
        ('emergency_fund', 'Fondo de Emergencia'),
        ('investment', 'Inversión'),
        ('budget_optimization', 'Optimización de Presupuesto'),
        ('savings_habit', 'Hábito de Ahorro'),
        ('goal_prioritization', 'Priorización de Metas'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('critical', 'Crítica'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_recommendations')
    savings_goal = models.ForeignKey(SavingsGoal, on_delete=models.CASCADE, related_name='recommendations', null=True, blank=True)
    recommendation_type = models.CharField(max_length=25, choices=RECOMMENDATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Datos específicos de la recomendación
    estimated_savings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    implementation_difficulty = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    time_to_implement = models.IntegerField(default=0, help_text='Días estimados para implementar')
    
    # Datos adicionales
    category_id = models.IntegerField(null=True, blank=True, help_text='ID de categoría relacionada')
    action_items = models.JSONField(default=list, blank=True, help_text='Lista de acciones específicas')
    
    # Estado de la recomendación
    is_read = models.BooleanField(default=False)
    is_implemented = models.BooleanField(default=False)
    implemented_at = models.DateTimeField(null=True, blank=True)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return f'{self.title} - {self.user.username}'

    def mark_as_read(self):
        """Marca la recomendación como leída"""
        self.is_read = True
        self.save()

    def mark_as_implemented(self):
        """Marca la recomendación como implementada"""
        self.is_implemented = True
        self.implemented_at = timezone.now()
        self.save()


class SavingsInsight(models.Model):
    """Modelo para insights y análisis de ahorro"""
    INSIGHT_TYPE_CHOICES = (
        ('spending_pattern', 'Patrón de Gastos'),
        ('savings_rate', 'Tasa de Ahorro'),
        ('goal_progress', 'Progreso de Meta'),
        ('budget_variance', 'Variación de Presupuesto'),
        ('income_analysis', 'Análisis de Ingresos'),
        ('savings_trend', 'Tendencia de Ahorro'),
        ('goal_risk', 'Riesgo de Meta'),
        ('optimization_opportunity', 'Oportunidad de Optimización'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_insights')
    insight_type = models.CharField(max_length=25, choices=INSIGHT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Datos del insight
    data = models.JSONField(default=dict)
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.user.username}'


class SavingsAchievement(models.Model):
    """Modelo para sistema de gamificación y logros"""
    ACHIEVEMENT_TYPE_CHOICES = (
        ('goal_completed', 'Meta Completada'),
        ('savings_streak', 'Racha de Ahorro'),
        ('milestone_reached', 'Hito Alcanzado'),
        ('habit_formed', 'Hábito Formado'),
        ('smart_saver', 'Ahorrador Inteligente'),
        ('budget_master', 'Maestro del Presupuesto'),
        ('emergency_fund', 'Fondo de Emergencia'),
        ('first_goal', 'Primera Meta'),
        ('savings_champion', 'Campeón del Ahorro'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_achievements')
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    points = models.IntegerField(default=0, help_text='Puntos otorgados por el logro')
    
    # Datos del logro
    data = models.JSONField(default=dict, blank=True)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.user.username}'


class SavingsSimulation(models.Model):
    """Modelo para simulaciones de ahorro"""
    SIMULATION_TYPE_CHOICES = (
        ('spending_reduction', 'Reducción de Gastos'),
        ('income_increase', 'Aumento de Ingresos'),
        ('goal_adjustment', 'Ajuste de Meta'),
        ('savings_increase', 'Aumento de Ahorro'),
        ('scenario_comparison', 'Comparación de Escenarios'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_simulations')
    simulation_type = models.CharField(max_length=20, choices=SIMULATION_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Parámetros de la simulación
    parameters = models.JSONField(default=dict)
    
    # Resultados de la simulación
    results = models.JSONField(default=dict)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    is_saved = models.BooleanField(default=False, help_text='Si la simulación fue guardada por el usuario')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.user.username}'


class SavingsReminder(models.Model):
    """Modelo para recordatorios inteligentes"""
    REMINDER_TYPE_CHOICES = (
        ('savings_due', 'Ahorro Pendiente'),
        ('goal_at_risk', 'Meta en Riesgo'),
        ('milestone_approaching', 'Hito Cercano'),
        ('habit_reminder', 'Recordatorio de Hábito'),
        ('budget_alert', 'Alerta de Presupuesto'),
        ('achievement_unlocked', 'Logro Desbloqueado'),
    )
    
    PRIORITY_CHOICES = (
        ('low', 'Baja'),
        ('medium', 'Media'),
        ('high', 'Alta'),
        ('urgent', 'Urgente'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='savings_reminders')
    reminder_type = models.CharField(max_length=25, choices=REMINDER_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Configuración de recordatorio
    scheduled_for = models.DateTimeField()
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.JSONField(default=dict, blank=True)
    
    # Estado
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)
    is_dismissed = models.BooleanField(default=False)
    dismissed_at = models.DateTimeField(null=True, blank=True)
    
    # Datos relacionados
    related_goal_id = models.IntegerField(null=True, blank=True)
    related_transaction_id = models.IntegerField(null=True, blank=True)
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['scheduled_for']

    def __str__(self):
        return f'{self.title} - {self.user.username}'

    def send(self):
        """Marca el recordatorio como enviado"""
        self.is_sent = True
        self.sent_at = timezone.now()
        self.save()

    def dismiss(self):
        """Marca el recordatorio como descartado"""
        self.is_dismissed = True
        self.dismissed_at = timezone.now()
        self.save()
