from django.urls import path, include
from rest_framework import routers

from .api.basket import BasketView
from .api.catalog import CategoriesListView, LimitedProductsView, BannersProductsView, \
    PopularProductsView, SalesView, CatalogView
from .api.order import OrderView, OrderDetailView
from .api.payment import PaymentView
from .api.product import ProductDetailView, ReviewCreateView
from .api.tag import TagListView


urlpatterns = [
    path("categories/", CategoriesListView.as_view(), name="categories"),
    path(
        "product/",
        include(
            [
                path("<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
                path(
                    "<int:pk>/reviews/",
                    ReviewCreateView.as_view(),
                    name="create-review",
                ),
            ]
        ),
    ),
    path("basket/", BasketView.as_view(), name="basket"),
    path("orders/", OrderView.as_view(), name="orders"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="orders"),
    path("payment/<int:pk>/", PaymentView.as_view(), name="payment"),
]


router = routers.SimpleRouter()
# ВАЖНО: т.к. в представлениях нет queryset / get_queryset(), то basename обязательно!
router.register(r"products/limited", LimitedProductsView, basename="limited-products")
router.register(r"banners", BannersProductsView, basename="banner")
router.register(r"products/popular", PopularProductsView, basename="popular-products")
router.register(r"sales", SalesView, basename="sales")
router.register(r"catalog", CatalogView, basename="catalog")
router.register(r"tags", TagListView, basename="tags")

urlpatterns += router.urls
