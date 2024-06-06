
from flask import session

def clear_all_sessions():
    """
    This function clears all sessions.
    """
    session.clear()
    session.pop('user_secret_code', default=None)
    session.pop('activate_token', default=None)
    session.pop('user_df', default=None)
    session.pop('user_secret_code', default=None)
    session.pop('two_fa_auth_method', default=None)
    session.pop('otpqrcode', default=None)
    session.pop('otpqrcode_uri', default=None)
    session.pop('user_id', default=None)
    
    return session