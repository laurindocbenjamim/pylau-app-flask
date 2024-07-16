

from flask import Blueprint
from .product_view import ProductView
from .product_delete_view import DeleteProductView
from .productModel import Product

bp_product = Blueprint('stock', __name__, url_prefix='/stock')
bp_product.add_url_rule('/product', view_func=ProductView.as_view('product', Product,''))
bp_product.add_url_rule('/product/<int:id>', view_func=ProductView.as_view('product_by_id', Product,''))
bp_product.add_url_rule('/product/<int:id>/update', view_func=ProductView.as_view('product_update', Product,''))

bp_product.add_url_rule('/product/<int:id>/delete', view_func=DeleteProductView.as_view('product_update', Product,''))