from products.views.product_view import *  # noqa
from products.views.product_view import __all__ as product_view_all
from products.views.label_view import *  # noqa
from products.views.label_view import __all__ as label_view_all
from products.views.stock_view import *  # noqa
from products.views.stock_view import __all__ as stock_view_all

__all__ = [
    *product_view_all,
    *label_view_all,
    *stock_view_all,
]
