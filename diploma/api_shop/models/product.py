import logging

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Avg
from django.core.cache import cache

from .category import Category
from .review import Review
from .tag import Tag


class Product(models.Model):
    """
    Модель для хранения данных о товарах
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="категория",
    )
    price = models.FloatField(validators=[MinValueValidator(0)], verbose_name="цена")
    count = models.PositiveIntegerField(default=0, verbose_name="кол-во")
    date = models.DateTimeField(auto_now_add=True, verbose_name="время добавления")
    title = models.CharField(max_length=250, verbose_name="название")
    short_description = models.CharField(
        max_length=500, verbose_name="краткое описание"
    )
    description = models.TextField(max_length=1000, verbose_name="описание")
    tags = models.ManyToManyField(Tag, related_name="products", verbose_name="теги")

    @property
    def reviews_count(self) -> int:
        """
        Кол-во отзывов у товара
        """
        return self.reviews.count()

    def free_delivery(self) -> bool:
        """
        Определение стоимости доставки в зависимости от стоимости товара
        """
        if self.price > 2000:
            return True
        return False

    @property
    def average_rating(self) -> int:
        """
        Расчет средней оценки товара на основе всех отзывов
        """
        res = cache.get_or_set(
            f"average_rating_{self.id}",
            Review.objects.filter(product_id=self.id).aggregate(
                average_rate=Avg("rate")
            ),
        )

        try:
            # Округляем рейтинг товара до 1 знака после запятой
            return round(res["average_rate"], 1)
        except TypeError:
            return 0

    class Meta:
        db_table = "products"
        verbose_name = "товар"
        verbose_name_plural = "товары"
        ordering = ["id"]

    def add_tags(self, *args, **kwargs):
        """
        Добавляем запись об используемых тегах в категорию товара
        (для быстрого вывода всех тегов товаров определенной категории)
        """
        chair_tags = self.category.tags.all()

        for tag in self.tags.all():
            if tag not in chair_tags:
                self.category.tags.add(tag)

        super(Product, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Сохранение тегов и очистка кэша при сохранении и изменении товара
        """

        try:
            self.add_tags()

        except ValueError:
            super(Product, self).save(*args, **kwargs)
            self.add_tags()


    def __str__(self) -> str:
        return str(self.title)
