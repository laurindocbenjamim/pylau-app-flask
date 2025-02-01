
import sys
import traceback
from flask import render_template, make_response, json, redirect, url_for
from flask_wtf.csrf import CSRFError
from ...configs_package.modules.logger_config import logger, get_message

def error_handlers_view(app):

    # Error handling for file too large
    @app.errorhandler(413)
    def request_entity_too_large(error):
        app.logger.error('File is too large. %s', error)
        return f"File is too large. The maximum size is {app.config['MAX_CONTENT_LENGTH']}MB.", 413
    
    @app.errorhandler(404)
    def page_not_found(e):

        app.logger.error('Page not found: %s', e)
        image = "https://atlassianblog.wpengine.com/wp-content/uploads/2017/12/44-incredible-404-error-pages@3x.png"
        title = f"{e.code} {e.name}"
        error_code=e.code
        error_description = e.name
        message = "Oops! Something went wrong on our end. Please try again later."
        response = e.get_response()
        # replace the body with JSON
        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"

        response = make_response(render_template('errors/errors.html', title=title, message=message, error_description=error_description, 
                                             image=image, error_code=error_code), 404)
        response.headers['X-Something'] = 'Page Not Found'
        from ..config_headers import set_header_params
        set_header_params(response)
        get_message(e, type='debug')

        return response
    
    @app.errorhandler(500)
    def page_not_found(e):

        title = f"{e.code} {e.name}"
        error_code=e.code
        error_description = e.description
        message = "Oops! Something went wrong on our end. Please try again later."
        # Log the error
        app.logger.error('Internal Server Error: %s', e)
        image='https://static.doofinder.com/main-files/uploads/2019/09/error-500-doofinder.jpg'
        # Render the error page
        response = make_response(render_template('errors/errors.html', title=title, message=message, error_description=error_description, 
                                             image=image, error_code=error_code), 500)
        response.headers['X-Something'] = 'Internal Server Error'
        from ..config_headers import set_header_params
        set_header_params(response)
        get_message(e, type='debug')
        
        return response
    
    @app.errorhandler(Exception)
    def handle_generic_error(e):
        title = "General error"
        error_code="Exp."
        error_description = f"An exception occurred {e}"
        message = "Oops! Something went wrong on our end. Please try again later."
        app.logger.error('Internal Server Error: %s', e)
        image=image='https://miro.medium.com/v2/resize:fit:1400/1*2Z41mMgjOxkUUuvIwd7Djw.png'
        response = make_response(render_template('errors/errors.html', title=title, message=message, error_description=error_description, 
                                             image=image, error_code=error_code), 500)
        response.headers['X-Something'] = 'Generic Error'
        from ..config_headers import set_header_params
        set_header_params(response)
        get_message(e, type='debug')
        
        return response

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        #return render_template('csrf_error.html', reason=e.description), 400
        title = f"{e.code} {e.name}"
        error_code=e.code
        error_description = e.name
        message = f'X-CSRFToken error. {e.description}'
        image=image='https://www.prontomarketing.com/wp-content/uploads/2022/12/how-to-fix-400-bad-requst-error-wordpress.png'
        #resp = make_response(render_template('errors/400.html', message=f"{e.code} -{e.name}. Unauthorized 
        #                                     {e.description}", image=image, error_code=error_code), 400)
        response = make_response(render_template('errors/errors.html', title=title, message=message, error_description=error_description, 
                                             image=image, error_code=error_code), 400)
        response.headers['X-Something'] = 'Unauthorized'
        from ..config_headers import set_header_params
        set_header_params(response)

        get_message(e, type='debug')
        
        return response

    @app.errorhandler(400)
    def handle_unauthorized_error(e):

        title = f"{e.code} {e.name}"
        error_code=e.code
        error_description = e.description
        message = "Oops! Something went wrong on our end. Please try again later."
        image=image='https://www.prontomarketing.com/wp-content/uploads/2022/12/how-to-fix-400-bad-requst-error-wordpress.png'
        #resp = make_response(render_template('errors/400.html', message=f"{e.code} -{e.name}. Unauthorized 
        #                                     {e.description}", image=image, error_code=error_code), 400)
        response = make_response(render_template('errors/errors.html', title=title, message=message, error_description=error_description, 
                                             image=image, error_code=error_code), 400)
        response.headers['X-Something'] = 'Unauthorized'
        from ..config_headers import set_header_params
        set_header_params(response)

        get_message(e, type='debug')
        
        return response
        #return redirect(url_for('auth.user.login'))
    
        
    @app.errorhandler(401)
    def handle_unauthorized_error(e):

        title = f"{e.code} {e.name}"
        error_code=e.code
        error_description = e.name
        message = "Oops! Something went wrong on our end. Please try again later."
        image=image='https://www.asktheegghead.com/wp-content/uploads/2019/12/401-error-wordpress-featured-image.jpg'
        response = make_response(render_template('errors/errors.html', title=title, message=message, error_description=error_description, 
                                             image=image, error_code=error_code), 401)
        response.headers['X-Something'] = 'Unauthorized'
        from ..config_headers import set_header_params
        set_header_params(response)
        get_message(e, type='debug')
       
        return response

    @app.errorhandler(403)
    def handle_forbidden_error(e):

        title = f"{e.code} {e.name}"
        error_code=e.code
        error_description = e.name
        message = "Oops! Something went wrong on our end. Please try again later."
        image='https://www.online-tech-tips.com/wp-content/uploads/2021/06/http-403.jpeg'
        response = make_response(render_template('errors/errors.html', title=title, message=message, error_description=error_description, 
                                             image=image, error_code=error_code), 403)
        response.headers['X-Something'] = 'Forbidden'
        from ..config_headers import set_header_params
        set_header_params(response)
        get_message(e, type='debug')
        
        return response
        #return redirect(url_for('auth.user.login'))

    @app.errorhandler(405)
    def handle_method_not_allowed_error(e):
        
        title = f"{e.code} {e.name}"
        error_code=e.code
        error_description = e.name
        message = "Oops! Something went wrong on our end. Please try again later."
        image='https://www.ionos.co.uk/digitalguide/fileadmin/DigitalGuide/Teaser/405-Method-Not-Allowed-t.jpg'
        response = make_response(render_template('errors/errors.html', title=title, message=message, error_description=error_description, 
                                             image=image, error_code=error_code), 405)
        response.headers['X-Something'] = 'Method Not Allowed'
        from ..config_headers import set_header_params
        set_header_params(response)
        get_message(e, type='debug')
        
        return response
    
    @app.errorhandler(503)
    def unavailable_service(e):

        title = f"{e.code} {e.name}"
        error_code=e.code
        error_description = e.name
        message = "Oops! Something went wrong on our end. Please try again later."
        image='https://www.lifewire.com/thmb/3Zne74PQmtY62N1E02VkiNg78bQ=/768x0/filters:no_upscale():max_bytes(150000):strip_icc()/shutterstock_717832600-Converted-5a29aaf3b39d030037b2cda9.png'
        response = make_response(render_template('errors/errors.html', title=title, message=message, error_description=error_description, 
                                             image=image, error_code=error_code), 503)
        response.headers['X-Something'] = 'Method Not Allowed'
        from ..config_headers import set_header_params
        set_header_params(response)
        get_message(e, type='debug')
        
        return response