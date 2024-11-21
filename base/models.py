from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    category = models.TextField(blank=True, null=True)
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        default='MEDIUM'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title