
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
        response.set_cookie('csrf_token', csrf_token)
        return response
    
    # Verify the CSRF token
    def verify_csrf_token(self,request):
        csrf_token = request.cookies.get('csrf_token')
        if not csrf_token or csrf_token != request.form.get('csrf_token'):
            return False
        return True
