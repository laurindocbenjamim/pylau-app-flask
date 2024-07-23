

from flask import Blueprint
from .module_product.product_post_put_view import ProductView
from .module_product.product_delete_view import DeleteProductView
from .module_product.productModel import Product
from .module_stock.stockModel import Stock
from .module_product.productDiscountModel import ProductDiscount
from .module_product.product_gets_view import ProductGetsView

bp_product = Blueprint('stock', __name__, url_prefix='/stock')
bp_product.add_url_rule('/product', view_func=ProductView.as_view('product', Product,''))
bp_product.add_url_rule('/product/select', view_func=ProductGetsView.as_view('product_select', Product,''))
bp_product.add_url_rule('/product/select/<int:id>', view_func=ProductGetsView.as_view('product_by_id', Product,''))
bp_product.add_url_rule('/product/<int:id>/update', view_func=ProductView.as_view('product_update', Product,''))
bp_product.add_url_rule('/product/<int:id>/delete', view_func=DeleteProductView.as_view('product_delete', Product,''))

# Importing the stock view and creatng the routes
from .module_stock import Stock
from .module_stock import StockPostPutView
bp_product.add_url_rule('/create/stock', view_func=StockPostPutView.as_view('create', Stock, ''))
#bp_product.add_url_rule('/product/<int:id>/delete', view_func=StockPostPutView.as_view('delete', Stock, ''))
bp_product.add_url_rule('/update/<string:product_barcode>/stock', view_func=StockPostPutView.as_view('update', Stock, ''))