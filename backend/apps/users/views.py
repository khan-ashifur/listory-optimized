from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        data = {
            'username': request.user.username,
            'email': request.user.email,
            'subscription_type': profile.subscription_type,
            'credits_remaining': profile.credits_remaining,
            'credits_used': profile.credits_used,
            'is_premium': profile.is_premium,
        }
        return Response(data)