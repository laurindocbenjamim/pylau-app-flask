

from flask import Blueprint
from .product_api import ProductAPI
from .productModel import Product

bp_product_api = Blueprint('stock', __name__, url_prefix='/stock')
bp_product_api.add_url_rule('/product', view_func=ProductAPI.as_view('product', Product))
bp_product_api.add_url_rule('/product/<int:id>', view_func=ProductAPI.as_view('product_by_id', Product))
bp_product_api.add_url_rule('/product/<int:id>/update', view_func=ProductAPI.as_view('product_update', Product))