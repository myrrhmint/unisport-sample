from django.urls import path
from products.views import (
    ProductLabelViewset,
    ProductViewset,
    StockViewset,
    LabelViewset,
)
from rest_framework_nested import routers
from django.urls import include

router = routers.DefaultRouter()
router.register(r"products", ProductViewset, basename="products")
router.register(r"labels", LabelViewset, basename="labels")

products_router = routers.NestedSimpleRouter(router, r"products", lookup="product")
products_router.register(r"labels", ProductLabelViewset, basename="product-labels")
products_router.register(r"stock", StockViewset, basename="product-stock")

app_name = "products"
urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),
]
