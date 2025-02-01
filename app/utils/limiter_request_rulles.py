

from app.dependencies import Limiter, current_app
from app.dependencies import get_remote_address

limiter = Limiter(
        get_remote_address,
        app=current_app,
        default_limits=["200 per day", "50 per hour"]
    )