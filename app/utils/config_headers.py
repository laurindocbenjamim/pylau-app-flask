from flask import make_response

def set_header_params(response: make_response):

    """  Content Security Policy (CSP)
        Tell the browser where it can load various types of resource from. This header should 
        be used whenever possible, but requires some work to define the correct policy for your site. 
        A very strict policy would be:
    """
    #response.headers['Content-Security-Policy'] = "default-src 'self'"

    """ HTTP Strict Transport Security (HSTS)
        Tells the browser to convert all HTTP requests to HTTPS, preventing man-in-the-middle (MITM) attacks.
    """

    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    """ X-Frame-Options
        Prevents external sites from embedding your site in an iframe. This prevents a class of attacks where clicks in the outer frame can be translated invisibly 
        to clicks on your page’s elements. This is also known as “clickjacking”.
    
    """
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'

    """ X-Content-Type-Options
        Forces the browser to honor the response content type instead of trying to detect it, which can be abused to generate a cross-site scripting (XSS) attack.
    """
    response.headers['X-Content-Type-Options'] = 'nosniff'

    