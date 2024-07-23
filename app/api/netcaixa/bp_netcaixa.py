


from flask import Blueprint

bp_netcaixa = Blueprint('netcaixa', __name__, url_prefix='/netcaixa')
from .bp_stock import bp_product

bp_netcaixa.register_blueprint(bp_product)