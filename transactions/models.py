from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta


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
