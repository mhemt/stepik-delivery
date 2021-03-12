from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer


class UserDetailView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
