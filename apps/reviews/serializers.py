from rest_framework import serializers

from apps.reviews.models import Review
from apps.users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'author', 'status', 'text', 'created_at', 'published_at']
        read_only_fields = ['author', 'status', 'created_at', 'published_at']

    def create(self, validated_data):
        author = self.context['request'].user
        text = validated_data['text']

        return Review.objects.create(
            author=author,
            text=text,
            status=Review.Status.MODERATION,
        )
