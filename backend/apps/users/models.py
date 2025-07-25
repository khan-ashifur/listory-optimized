from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    SUBSCRIPTION_TYPES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription_type = models.CharField(max_length=20, choices=SUBSCRIPTION_TYPES, default='free')
    credits_remaining = models.IntegerField(default=3)
    credits_used = models.IntegerField(default=0)
    subscription_start_date = models.DateTimeField(null=True, blank=True)
    subscription_end_date = models.DateTimeField(null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subscription_type}"

    @property
    def is_premium(self):
        return self.subscription_type in ['basic', 'pro', 'enterprise']