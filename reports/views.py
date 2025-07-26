from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer
from transactions.views import IsOwner

# Create your views here.

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.request.user.reports.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
