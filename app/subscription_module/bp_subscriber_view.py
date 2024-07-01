from flask import Blueprint
from .subscriberView import SubscriberView
from .subscriber import Subscriber

bp = Blueprint('subscriber', __name__, url_prefix='/subscriber')
bp.add_url_rule('/subscribe', view_func=lambda: SubscriberView('subscribe', Subscriber))

