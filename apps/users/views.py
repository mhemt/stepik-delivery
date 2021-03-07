from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.carts.models import Cart
from apps.users.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    model = get_user_model()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        super().perform_create(serializer)

        # Creating cart with new user
        user = get_user_model().objects.get(username=serializer.data['username'])
        Cart.objects.get_or_create(user_id=user.id)


class UserDetailView(RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.queryset.get(id=self.request.user.id)
