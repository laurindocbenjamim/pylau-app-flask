

from flask import Blueprint
from flask_cors import CORS

from .module_product.productModel import Product

bp_product = Blueprint('stock', __name__, url_prefix='/stock')
CORS(bp_product)
from .module_product.product_post_put_view import ProductView
from .module_product.product_delete_view import DeleteProductView
from .module_product.productDiscountModel import ProductDiscount
from .module_product.product_gets_view import ProductGetsView

bp_product.add_url_rule('/product', view_func=ProductView.as_view('product', Product,''))
bp_product.add_url_rule('/product/select', view_func=ProductGetsView.as_view('product_select', Product,''))
bp_product.add_url_rule('/product/select/<int:id>', view_func=ProductGetsView.as_view('product_by_id', Product,''))
bp_product.add_url_rule('/product/<int:id>/update', view_func=ProductView.as_view('product_update', Product,''))
bp_product.add_url_rule('/product/<int:id>/delete', view_func=DeleteProductView.as_view('product_delete', Product,''))

# Importing the stock view and creatng the routes
from .module_stock import Stock
from .module_stock import StockPostPutView
from .module_stock import StockDeleteProductView
from .module_stock import StockGetProductsView

bp_product.add_url_rule('/create/stock', view_func=StockPostPutView.as_view('create_stock', Stock, ''))
bp_product.add_url_rule('/update/<string:product_barcode>/stock', view_func=StockPostPutView.as_view('update_stock', Stock, ''))
bp_product.add_url_rule('/select/all', view_func=StockGetProductsView.as_view('select_stocks', Stock, ''))
bp_product.add_url_rule('/select/<int:id>', view_func=StockGetProductsView.as_view('get_stock', Stock, ''))
bp_product.add_url_rule('/select/by', view_func=StockGetProductsView.as_view('get_stocks_by', Stock, ''))
bp_product.add_url_rule('/delete/<item>/stock', view_func=StockDeleteProductView.as_view('delete_stock', Stock, ''))

# Importing the price of product view
# adn creating the routes
from .module_prices import ProductPricePostPutViev
from .module_prices import ProductPriceModel

bp_product.add_url_rule('/price/create', view_func=ProductPricePostPutViev.as_view('create_price', ProductPriceModel, ''))
bp_product.add_url_rule('/price/update/<string:product_barcode>', view_func=ProductPricePostPutViev.as_view('update_price', ProductPriceModel, ''))
bp_product.add_url_rule('/price/select/all', view_func=ProductPricePostPutViev.as_view('select_prices', ProductPriceModel, ''))
bp_product.add_url_rule('/price/select/<int:id>', view_func=ProductPricePostPutViev.as_view('get_price', ProductPriceModel, ''))
bp_product.add_url_rule('/price/select/by', view_func=ProductPricePostPutViev.as_view('get_price_by', ProductPriceModel, ''))
bp_product.add_url_rule('/price/delete/<item>', view_func=ProductPricePostPutViev.as_view('delete_price', ProductPriceModel, ''))




