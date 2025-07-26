from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Budget
from .serializers import BudgetSerializer
from transactions.views import IsOwner

# Create your views here.

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.request.user.budgets.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
