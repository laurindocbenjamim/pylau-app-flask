
from flask import Blueprint
bp_api = Blueprint('api', __name__, url_prefix='/api')


from .netcaixa import bp_netcaixa_api
bp_api.register_blueprint(bp_netcaixa_api)
