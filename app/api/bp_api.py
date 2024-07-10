
from flask import Blueprint
bp_api = Blueprint('api', __name__, url_prefix='/api')


from .netcaixa import bp_netcaixa
bp_api.register_blueprint(bp_netcaixa)
