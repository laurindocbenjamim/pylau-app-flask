
from flask import render_template, make_response

def error_handlers_view(app):
    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.error('Page not found: %s', e)
        image = "https://atlassianblog.wpengine.com/wp-content/uploads/2017/12/44-incredible-404-error-pages@3x.png"
        resp = make_response(render_template('errors/404.html', message="Page not found.", image=image, error=404), 404)
        resp.headers['X-Something'] = 'Page Not Found'
        return resp
    
    @app.errorhandler(500)
    def page_not_found(e):
        # Log the error
        app.logger.error('Internal Server Error: %s', e)
        image='https://static.doofinder.com/main-files/uploads/2019/09/error-500-doofinder.jpg'
        # Render the error page
        resp = make_response(render_template('errors/500.html', message="Internal Server Error", image=image, error=500), 500)
        resp.headers['X-Something'] = 'Internal Server Error'
        return resp
    
    @app.errorhandler(Exception)
    def handle_generic_error(e):
        app.logger.error('Internal Server Error: %s', e)
        image=image='https://miro.medium.com/v2/resize:fit:1400/1*2Z41mMgjOxkUUuvIwd7Djw.png'
        resp = make_response(render_template('errors/generic.html', message="An error occurred", image=image, error=500), 500)
        resp.headers['X-Something'] = 'Generic Error'
        return resp

    @app.errorhandler(401)
    def handle_unauthorized_error(e):
        image=image='https://media.giphy.com/media/3o7aTskHEUdgCQAXde/giphy.gif'
        resp = make_response(render_template('errors/401.html', message="Unauthorized", image=image, error=401), 401)
        resp.headers['X-Something'] = 'Unauthorized'
        return resp

    @app.errorhandler(403)
    def handle_forbidden_error(e):
        image='https://media.giphy.com/media/3o7aTskHEUdgCQAXde/giphy.gif'
        resp = make_response(render_template('errors/403.html', message="Forbidden", image=image, error=403), 403)
        resp.headers['X-Something'] = 'Forbidden'
        return resp

    @app.errorhandler(405)
    def handle_method_not_allowed_error(e):
        
        image='https://www.ionos.co.uk/digitalguide/fileadmin/DigitalGuide/Teaser/405-Method-Not-Allowed-t.jpg'
        resp = make_response(render_template('errors/405.html', message="Method Not Allowed", image=image, error=405), 405)
        resp.headers['X-Something'] = 'Method Not Allowed'
        return resp
    
    @app.errorhandler(503)
    def unavailable_service(e):
        image='https://www.lifewire.com/thmb/3Zne74PQmtY62N1E02VkiNg78bQ=/768x0/filters:no_upscale():max_bytes(150000):strip_icc()/shutterstock_717832600-Converted-5a29aaf3b39d030037b2cda9.png'
        resp = make_response(render_template('errors/503.html', message="Unavailable service", image=image, error=503), 503)
        resp.headers['X-Something'] = 'Method Not Allowed'
        return resp