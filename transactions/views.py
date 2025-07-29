from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import datetime, timedelta
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import (
    Category, Transaction, CategoryAnalysis, SavingsGoal, 
    SavingsTransaction, AutoSaveRule, SavingsRecommendation, 
    SavingsInsight, SavingsAchievement, SavingsSimulation, SavingsReminder
)
from .serializers import (
    CategorySerializer, TransactionSerializer, CategoryAnalysisSerializer,
    CategorySummarySerializer, CategoryTrendSerializer, CategoryComparisonSerializer,
    SavingsGoalSerializer, SavingsTransactionSerializer, AutoSaveRuleSerializer,
    SavingsRecommendationSerializer, SavingsInsightSerializer, SavingsAchievementSerializer,
    SavingsSimulationSerializer, SavingsReminderSerializer, SavingsDashboardSerializer
)

# Create your views here.

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

@extend_schema_view(
    list=extend_schema(
        summary="Listar categorías",
        description="Obtiene todas las categorías del usuario autenticado",
        tags=['categories']
    ),
    create=extend_schema(
        summary="Crear categoría",
        description="Crea una nueva categoría para el usuario autenticado",
        tags=['categories']
    ),
    retrieve=extend_schema(
        summary="Obtener categoría",
        description="Obtiene los detalles de una categoría específica",
        tags=['categories']
    ),
    update=extend_schema(
        summary="Actualizar categoría",
        description="Actualiza completamente una categoría existente",
        tags=['categories']
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente categoría",
        description="Actualiza parcialmente una categoría existente",
        tags=['categories']
    ),
    destroy=extend_schema(
        summary="Eliminar categoría",
        description="Elimina una categoría existente",
        tags=['categories']
    ),
)
class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar categorías de transacciones.
    
    Permite crear, leer, actualizar y eliminar categorías personalizadas
    que se utilizan para clasificar las transacciones.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.request.user.categories.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Análisis de categoría",
        description="Obtiene un análisis detallado de una categoría específica",
        parameters=[
            OpenApiParameter(
                name='start_date',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Fecha de inicio para el análisis (YYYY-MM-DD)',
                required=True
            ),
            OpenApiParameter(
                name='end_date',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Fecha de fin para el análisis (YYYY-MM-DD)',
                required=True
            ),
            OpenApiParameter(
                name='transaction_type',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Tipo de transacción a analizar (income/expense)',
                examples=[
                    OpenApiExample('Ingresos', value='income'),
                    OpenApiExample('Gastos', value='expense'),
                ]
            ),
        ],
        tags=['categories']
    )
    @action(detail=True, methods=['get'])
    def analysis(self, request, pk=None):
        """Obtiene un análisis detallado de una categoría específica"""
        try:
            category = self.get_object()
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            transaction_type = request.query_params.get('transaction_type')

            if not start_date or not end_date:
                return Response(
                    {'error': 'start_date y end_date son requeridos'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Obtener transacciones del período
            transactions = category.transactions.filter(
                date__range=[start_date, end_date]
            )

            if transaction_type:
                transactions = transactions.filter(transaction_type=transaction_type)

            # Calcular métricas
            total_income = transactions.filter(transaction_type='income').aggregate(
                total=Sum('amount'))['total'] or 0
            total_expenses = transactions.filter(transaction_type='expense').aggregate(
                total=Sum('amount'))['total'] or 0
            transaction_count = transactions.count()
            average_amount = transactions.aggregate(avg=Avg('amount'))['avg'] or 0

            # Calcular porcentajes del total
            total_user_income = Transaction.objects.filter(
                user=request.user,
                transaction_type='income',
                date__range=[start_date, end_date]
            ).aggregate(total=Sum('amount'))['total'] or 0

            total_user_expenses = Transaction.objects.filter(
                user=request.user,
                transaction_type='expense',
                date__range=[start_date, end_date]
            ).aggregate(total=Sum('amount'))['total'] or 0

            percentage_of_income = (total_income / total_user_income * 100) if total_user_income > 0 else 0
            percentage_of_expenses = (total_expenses / total_user_expenses * 100) if total_user_expenses > 0 else 0

            # Obtener última transacción
            last_transaction = transactions.order_by('-date').first()

            # Calcular tendencia (comparar con período anterior)
            start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
            period_days = (end_dt - start_dt).days

            previous_start = start_dt - timedelta(days=period_days)
            previous_end = start_dt - timedelta(days=1)

            previous_transactions = category.transactions.filter(
                date__range=[previous_start, previous_end]
            )
            if transaction_type:
                previous_transactions = previous_transactions.filter(transaction_type=transaction_type)

            previous_total = previous_transactions.aggregate(total=Sum('amount'))['total'] or 0
            current_total = total_income + total_expenses

            if previous_total > 0:
                trend_percentage = ((current_total - previous_total) / previous_total) * 100
                if trend_percentage > 5:
                    trend = 'up'
                elif trend_percentage < -5:
                    trend = 'down'
                else:
                    trend = 'stable'
            else:
                trend_percentage = 0
                trend = 'stable'

            # Obtener transacciones más importantes
            top_transactions = list(transactions.order_by('-amount')[:10].values(
                'id', 'amount', 'transaction_type', 'date', 'description'
            ))

            # Generar datos de tendencia por día/semana/mes
            trend_data = self._generate_trend_data(transactions, start_dt, end_dt)

            analysis_data = {
                'category_id': category.id,
                'category_name': category.name,
                'category_color': category.color,
                'category_icon': category.icon,
                'period': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'days': period_days
                },
                'metrics': {
                    'total_income': total_income,
                    'total_expenses': total_expenses,
                    'transaction_count': transaction_count,
                    'average_amount': average_amount,
                    'percentage_of_total_income': round(percentage_of_income, 2),
                    'percentage_of_total_expenses': round(percentage_of_expenses, 2),
                },
                'trend': {
                    'direction': trend,
                    'percentage': round(trend_percentage, 2),
                    'previous_period_total': previous_total,
                    'current_period_total': current_total
                },
                'last_transaction_date': last_transaction.date if last_transaction else None,
                'top_transactions': top_transactions,
                'trend_data': trend_data
            }

            return Response(analysis_data)

        except Category.DoesNotExist:
            return Response(
                {'error': 'Categoría no encontrada'},
                status=status.HTTP_404_NOT_FOUND
            )

    def _generate_trend_data(self, transactions, start_date, end_date):
        """Genera datos de tendencia para gráficos"""
        # Agrupar por día
        daily_data = {}
        current_date = start_date
        
        while current_date <= end_date:
            daily_data[current_date.strftime('%Y-%m-%d')] = {
                'income': 0,
                'expense': 0,
                'total': 0
            }
            current_date += timedelta(days=1)

        # Llenar datos reales
        for transaction in transactions:
            date_str = transaction.date.strftime('%Y-%m-%d')
            if date_str in daily_data:
                if transaction.transaction_type == 'income':
                    daily_data[date_str]['income'] += float(transaction.amount)
                else:
                    daily_data[date_str]['expense'] += float(transaction.amount)
                daily_data[date_str]['total'] += float(transaction.amount)

        return {
            'daily': daily_data,
            'summary': {
                'total_days': len(daily_data),
                'days_with_transactions': len([d for d in daily_data.values() if d['total'] > 0]),
                'average_daily_income': sum(d['income'] for d in daily_data.values()) / len(daily_data),
                'average_daily_expense': sum(d['expense'] for d in daily_data.values()) / len(daily_data),
            }
        }

    @extend_schema(
        summary="Resumen de todas las categorías",
        description="Obtiene un resumen de todas las categorías del usuario con métricas",
        parameters=[
            OpenApiParameter(
                name='start_date',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Fecha de inicio para el análisis (YYYY-MM-DD)',
                required=True
            ),
            OpenApiParameter(
                name='end_date',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Fecha de fin para el análisis (YYYY-MM-DD)',
                required=True
            ),
            OpenApiParameter(
                name='transaction_type',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Tipo de transacción a analizar (income/expense)',
                examples=[
                    OpenApiExample('Ingresos', value='income'),
                    OpenApiExample('Gastos', value='expense'),
                ]
            ),
            OpenApiParameter(
                name='limit',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Número máximo de categorías a retornar (por defecto: 10)'
            ),
        ],
        tags=['categories']
    )
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Obtiene un resumen de todas las categorías con métricas"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        transaction_type = request.query_params.get('transaction_type')
        limit = int(request.query_params.get('limit', 10))

        if not start_date or not end_date:
            return Response(
                {'error': 'start_date y end_date son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )

        categories = self.get_queryset()
        summaries = []

        # Calcular totales del usuario
        user_transactions = Transaction.objects.filter(
            user=request.user,
            date__range=[start_date, end_date]
        )

        if transaction_type:
            user_transactions = user_transactions.filter(transaction_type=transaction_type)

        total_user_income = user_transactions.filter(transaction_type='income').aggregate(
            total=Sum('amount'))['total'] or 0
        total_user_expenses = user_transactions.filter(transaction_type='expense').aggregate(
            total=Sum('amount'))['total'] or 0

        for category in categories:
            # Obtener transacciones de la categoría
            category_transactions = category.transactions.filter(
                date__range=[start_date, end_date]
            )

            if transaction_type:
                category_transactions = category_transactions.filter(transaction_type=transaction_type)

            # Calcular métricas
            total_income = category_transactions.filter(transaction_type='income').aggregate(
                total=Sum('amount'))['total'] or 0
            total_expenses = category_transactions.filter(transaction_type='expense').aggregate(
                total=Sum('amount'))['total'] or 0
            transaction_count = category_transactions.count()
            average_amount = category_transactions.aggregate(avg=Avg('amount'))['avg'] or 0

            # Calcular porcentajes
            percentage_of_income = (total_income / total_user_income * 100) if total_user_income > 0 else 0
            percentage_of_expenses = (total_expenses / total_user_expenses * 100) if total_user_expenses > 0 else 0

            # Obtener última transacción
            last_transaction = category_transactions.order_by('-date').first()

            # Calcular tendencia simple
            if transaction_type:
                main_amount = total_income if transaction_type == 'income' else total_expenses
            else:
                main_amount = total_expenses  # Por defecto mostrar gastos

            summaries.append({
                'category_id': category.id,
                'category_name': category.name,
                'category_color': category.color,
                'category_icon': category.icon,
                'total_income': total_income,
                'total_expenses': total_expenses,
                'transaction_count': transaction_count,
                'average_amount': average_amount,
                'percentage_of_total_expenses': round(percentage_of_expenses, 2),
                'percentage_of_total_income': round(percentage_of_income, 2),
                'last_transaction_date': last_transaction.date if last_transaction else None,
                'trend': 'stable'  # Simplificado por ahora
            })

        # Ordenar por monto principal y limitar
        if transaction_type:
            summaries.sort(key=lambda x: x['total_income'] if transaction_type == 'income' else x['total_expenses'], reverse=True)
        else:
            summaries.sort(key=lambda x: x['total_expenses'], reverse=True)

        summaries = summaries[:limit]

        return Response({
            'period': {
                'start_date': start_date,
                'end_date': end_date
            },
            'categories': summaries,
            'totals': {
                'total_income': total_user_income,
                'total_expenses': total_user_expenses,
                'net_savings': total_user_income - total_user_expenses
            }
        })


@extend_schema_view(
    list=extend_schema(
        summary="Listar transacciones",
        description="Obtiene todas las transacciones del usuario autenticado",
        parameters=[
            OpenApiParameter(
                name='transaction_type',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filtrar por tipo de transacción (income/expense)',
                examples=[
                    OpenApiExample('Ingresos', value='income'),
                    OpenApiExample('Gastos', value='expense'),
                ]
            ),
            OpenApiParameter(
                name='category',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Filtrar por ID de categoría'
            ),
            OpenApiParameter(
                name='date_from',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Filtrar transacciones desde esta fecha (YYYY-MM-DD)'
            ),
            OpenApiParameter(
                name='date_to',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Filtrar transacciones hasta esta fecha (YYYY-MM-DD)'
            ),
        ],
        tags=['transactions']
    ),
    create=extend_schema(
        summary="Crear transacción",
        description="Crea una nueva transacción (ingreso o gasto) para el usuario autenticado",
        examples=[
            OpenApiExample(
                'Ingreso',
                value={
                    'category': 1,
                    'transaction_type': 'income',
                    'amount': '1500.00',
                    'date': '2024-01-15',
                    'description': 'Salario mensual'
                }
            ),
            OpenApiExample(
                'Gasto',
                value={
                    'category': 2,
                    'transaction_type': 'expense',
                    'amount': '50.00',
                    'date': '2024-01-15',
                    'description': 'Compra de comestibles'
                }
            ),
        ],
        tags=['transactions']
    ),
    retrieve=extend_schema(
        summary="Obtener transacción",
        description="Obtiene los detalles de una transacción específica",
        tags=['transactions']
    ),
    update=extend_schema(
        summary="Actualizar transacción",
        description="Actualiza completamente una transacción existente",
        tags=['transactions']
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente transacción",
        description="Actualiza parcialmente una transacción existente",
        tags=['transactions']
    ),
    destroy=extend_schema(
        summary="Eliminar transacción",
        description="Elimina una transacción existente",
        tags=['transactions']
    ),
)
class TransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar transacciones financieras.
    
    Permite crear, leer, actualizar y eliminar transacciones (ingresos y gastos)
    con categorización y fechas específicas.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        queryset = self.request.user.transactions.all()
        
        # Filtros opcionales
        transaction_type = self.request.query_params.get('transaction_type', None)
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
            
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category_id=category)
            
        date_from = self.request.query_params.get('date_from', None)
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
            
        date_to = self.request.query_params.get('date_to', None)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Estadísticas de transacciones",
        description="Obtiene estadísticas generales de las transacciones del usuario",
        parameters=[
            OpenApiParameter(
                name='start_date',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Fecha de inicio para las estadísticas (YYYY-MM-DD)'
            ),
            OpenApiParameter(
                name='end_date',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Fecha de fin para las estadísticas (YYYY-MM-DD)'
            ),
        ],
        tags=['transactions']
    )
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Obtiene estadísticas generales de las transacciones"""
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        queryset = self.get_queryset()

        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        # Estadísticas generales
        total_income = queryset.filter(transaction_type='income').aggregate(
            total=Sum('amount'))['total'] or 0
        total_expenses = queryset.filter(transaction_type='expense').aggregate(
            total=Sum('amount'))['total'] or 0
        total_transactions = queryset.count()
        average_transaction = queryset.aggregate(avg=Avg('amount'))['avg'] or 0

        # Estadísticas por categoría
        category_stats = queryset.values('category__name', 'category__color').annotate(
            total=Sum('amount'),
            count=Count('id'),
            avg_amount=Avg('amount')
        ).order_by('-total')

        # Transacciones más recientes
        recent_transactions = list(queryset.order_by('-date')[:5].values(
            'id', 'amount', 'transaction_type', 'date', 'description', 'category__name'
        ))

        # Transacciones más grandes
        largest_transactions = list(queryset.order_by('-amount')[:5].values(
            'id', 'amount', 'transaction_type', 'date', 'description', 'category__name'
        ))

        return Response({
            'summary': {
                'total_income': total_income,
                'total_expenses': total_expenses,
                'net_savings': total_income - total_expenses,
                'total_transactions': total_transactions,
                'average_transaction': average_transaction,
            },
            'by_category': category_stats,
            'recent_transactions': recent_transactions,
            'largest_transactions': largest_transactions,
            'period': {
                'start_date': start_date,
                'end_date': end_date
            }
        })


# ============================================================================
# VISTAS PARA EL SISTEMA DE AHORRO INTELIGENTE
# ============================================================================

class SavingsGoalViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar metas de ahorro inteligentes.
    """
    serializer_class = SavingsGoalSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.request.user.savings_goals.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Dashboard de ahorro",
        description="Obtiene un dashboard completo con todas las metas y estadísticas de ahorro",
        tags=['savings']
    )
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        """Obtiene el dashboard de ahorro del usuario"""
        user = request.user
        
        goals = self.get_queryset()
        
        total_savings = goals.aggregate(total=Sum('current_amount'))['total'] or 0
        total_goals = goals.count()
        active_goals = goals.filter(status='active').count()
        completed_goals = goals.filter(status='completed').count()
        
        current_month_start = timezone.now().date().replace(day=1)
        current_month_income = Transaction.objects.filter(
            user=user,
            transaction_type='income',
            date__gte=current_month_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        current_month_savings = SavingsTransaction.objects.filter(
            savings_goal__user=user,
            transaction_type='deposit',
            date__gte=current_month_start
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        monthly_savings_rate = (current_month_savings / current_month_income * 100) if current_month_income > 0 else 0
        
        recent_recommendations = SavingsRecommendation.objects.filter(
            user=user,
            is_read=False
        ).order_by('-priority', '-created_at')[:5]
        
        insights = SavingsInsight.objects.filter(
            user=user,
            is_archived=False
        ).order_by('-created_at')[:3]
        
        dashboard_data = {
            'total_savings': total_savings,
            'total_goals': total_goals,
            'active_goals': active_goals,
            'completed_goals': completed_goals,
            'monthly_savings_rate': round(monthly_savings_rate, 2),
            'goals_progress': SavingsGoalSerializer(goals, many=True).data,
            'recent_recommendations': SavingsRecommendationSerializer(recent_recommendations, many=True).data,
            'insights': SavingsInsightSerializer(insights, many=True).data
        }
        
        return Response(dashboard_data)


class SavingsTransactionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar transacciones de ahorro.
    """
    serializer_class = SavingsTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavingsTransaction.objects.filter(savings_goal__user=self.request.user)


class AutoSaveRuleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar reglas de ahorro automático.
    """
    serializer_class = AutoSaveRuleSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.request.user.auto_save_rules.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavingsRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para gestionar recomendaciones de ahorro.
    """
    serializer_class = SavingsRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.request.user.savings_recommendations.all()

    @extend_schema(
        summary="Marcar como leída",
        description="Marca una recomendación como leída",
        tags=['savings']
    )
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """Marca una recomendación como leída"""
        recommendation = self.get_object()
        recommendation.mark_as_read()
        return Response({'status': 'success'})

    @extend_schema(
        summary="Marcar como implementada",
        description="Marca una recomendación como implementada",
        tags=['savings']
    )
    @action(detail=True, methods=['post'])
    def mark_as_implemented(self, request, pk=None):
        """Marca una recomendación como implementada"""
        recommendation = self.get_object()
        recommendation.mark_as_implemented()
        return Response({'status': 'success'})


class SavingsInsightViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para gestionar insights de ahorro.
    """
    serializer_class = SavingsInsightSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.request.user.savings_insights.all()


class SavingsAchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para gestionar logros de ahorro.
    """
    serializer_class = SavingsAchievementSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.request.user.savings_achievements.all()


class SavingsSimulationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar simulaciones de ahorro.
    """
    serializer_class = SavingsSimulationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.request.user.savings_simulations.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavingsReminderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar recordatorios de ahorro.
    """
    serializer_class = SavingsReminderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.request.user.savings_reminders.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        summary="Enviar recordatorio",
        description="Marca un recordatorio como enviado",
        tags=['savings']
    )
    @action(detail=True, methods=['post'])
    def send(self, request, pk=None):
        """Marca un recordatorio como enviado"""
        reminder = self.get_object()
        reminder.send()
        return Response({'status': 'success'})

    @extend_schema(
        summary="Descartar recordatorio",
        description="Marca un recordatorio como descartado",
        tags=['savings']
    )
    @action(detail=True, methods=['post'])
    def dismiss(self, request, pk=None):
        """Marca un recordatorio como descartado"""
        reminder = self.get_object()
        reminder.dismiss()
        return Response({'status': 'success'})
