from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, TransactionViewSet, SavingsGoalViewSet, 
    SavingsTransactionViewSet, AutoSaveRuleViewSet, SavingsRecommendationViewSet,
    SavingsInsightViewSet, SavingsAchievementViewSet, SavingsSimulationViewSet,
    SavingsReminderViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'savings/goals', SavingsGoalViewSet, basename='savings-goals')
router.register(r'savings/transactions', SavingsTransactionViewSet, basename='savings-transactions')
router.register(r'savings/rules', AutoSaveRuleViewSet, basename='auto-save-rules')
router.register(r'savings/recommendations', SavingsRecommendationViewSet, basename='savings-recommendations')
router.register(r'savings/insights', SavingsInsightViewSet, basename='savings-insights')
router.register(r'savings/achievements', SavingsAchievementViewSet, basename='savings-achievements')
router.register(r'savings/simulations', SavingsSimulationViewSet, basename='savings-simulations')
router.register(r'savings/reminders', SavingsReminderViewSet, basename='savings-reminders')

urlpatterns = [
    path('', include(router.urls)),
] 