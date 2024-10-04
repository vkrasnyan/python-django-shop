from rest_framework import serializers

from ..models.tag import Tag


class TagSerializer(serializers.ModelSerializer):
    """
    Схема для тегов
    """

    class Meta:
        model = Tag
        fields = ["id", "name"]
