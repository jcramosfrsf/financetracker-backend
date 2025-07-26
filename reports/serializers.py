from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'user', 'name', 'report_type', 'start_date', 'end_date', 'generated_at', 'data'] 