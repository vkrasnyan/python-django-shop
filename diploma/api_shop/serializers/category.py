from rest_framework import serializers

from ..models.category import Category
from .image import ImageSerializer


class SubCategorySerializer(serializers.ModelSerializer):
    """
    Схема для вложенной категорий товаров
    """

    image = ImageSerializer()  # Вложенная схема с изображением

    class Meta:
        model = Category
        fields = ["id", "title", "image"]


class CategorySerializer(SubCategorySerializer):
    """
    Схема для категорий товаров
    """

    subcategories = SubCategorySerializer(
        many=True
    )  # Вложенная схема (подкатегория товаров)

    class Meta:
        model = Category
        fields = ["id", "title", "image", "subcategories"]
