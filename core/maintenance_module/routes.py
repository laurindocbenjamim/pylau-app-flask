
from flask import Blueprint, request, jsonify

bp = Blueprint("maintenance", __name__, url_prefix='/maintenance')

from core.maintenance_module.maintenance_route import maintenance_route

maintenance_route(bp)