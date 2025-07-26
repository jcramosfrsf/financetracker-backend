from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Report(models.Model):
    REPORT_TYPE_CHOICES = (
        ('monthly_summary', 'Monthly Summary'),
        ('spending_by_category', 'Spending by Category'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    generated_at = models.DateTimeField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return self.name
