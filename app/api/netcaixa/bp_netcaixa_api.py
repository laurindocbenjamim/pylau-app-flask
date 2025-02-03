


from flask import Blueprint

bp_netcaixa_api = Blueprint('netcaixa', __name__, url_prefix='/netcaixa')
from app.api.netcaixa.module_product.bp_product_api import bp_product_api

bp_netcaixa_api.register_blueprint(bp_product_api)