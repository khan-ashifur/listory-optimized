from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subscription_type', 'credits_remaining', 'credits_used', 'created_at')
    list_filter = ('subscription_type', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at',)