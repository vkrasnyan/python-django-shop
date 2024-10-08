import logging
from datetime import datetime
from django.db import models

from .product import Product


logger = logging.getLogger(__name__)


class SaleItem(models.Model):
    """
    Модель для хранения данных о скидках на товары
    """

    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, verbose_name="товар"
    )
    sale_price = models.FloatField(verbose_name="цена со скидкой")
    date_from = models.DateTimeField(verbose_name="дата начала распродажи")
    date_to = models.DateTimeField(verbose_name="дата окончания распродажи")


    @property
    def discount(self) -> int:
        """
        Скидка на товар
        """
        return 100 - int((self.sale_price / self.product.price) * 100)

    class Meta:
        db_table = "sales_items"
        verbose_name = "распродажа"
        verbose_name_plural = "распродажи"
        ordering = ["-date_to"]

    def __str__(self) -> str:
        return self.product.title


    def save(self, *args, **kwargs):
        """
        Автоматически удаляем запись (мягкое удаление), если срок распродажи вышел
        """
        current_date = datetime.now()

        if self.date_to.replace(tzinfo=None) <= current_date.replace(tzinfo=None):
            logger.warning("Срок распродажи товара закончился")
            self.deleted = True

        super(SaleItem, self).save(*args, **kwargs)
