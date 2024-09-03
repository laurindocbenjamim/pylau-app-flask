
import secrets


class MySecureUtils(object):
    """
    This class is sets as the security factory
    with all the rules that can garanteer safety 
    request and provent malicious attacks

    """
    # Generate a random CSRF token
    def generate_csrf_token(self):
        return secrets.token_hex(16)

    # Store the CSRF token in a cookie
    def set_csrf_cookie(self,response):
        csrf_token = self.generate_csrf_token()
        response.set_cookie('csrf_cookie', csrf_token)
        return csrf_token
    
    # Verify the CSRF token
    def verify_csrf_token(self,request):
        app_csrf_form = request.form.get('csrf_token')
        if app_csrf_form is None:
            return False
        csrf_token = request.cookies.get('csrf_cookie')
        if not csrf_token or csrf_token != request.form.get('csrf_cookie'):
            return False
        return True
