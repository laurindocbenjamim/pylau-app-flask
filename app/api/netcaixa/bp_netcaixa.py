


from flask import Blueprint

bp_netcaixa = Blueprint('netcaixa', __name__, url_prefix='/netcaixa')
from .module_product.bp_product import bp_product

bp_netcaixa.register_blueprint(bp_product)