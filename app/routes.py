import os
import secrets
from flask import Flask, render_template, request, session, jsonify
from flask_cors import cross_origin

def load_routes(app, db, login_manager):
    
     # Main route
    @app.route('/')
    def index():
        return render_template('site_home.html')
    
    from .views.error_handlers_view import error_handlers_view
    error_handlers_view(app)
    
    
    @app.route('/get-secret', methods=['GET'])
    @cross_origin(methods=['GET'])
    def get_secret():
            
        foo = secrets.token_urlsafe(32)
            
        return {'secret': foo}
    
    # Integrating the blueprints parent and child into the application

    from .auth_login_module import init_auth_login_view_app, bp_auth_login_view_child
    from .user_module import bp_auth_register_parent, init_user_register_app
    
    init_user_register_app()
    init_auth_login_view_app(login_manager=login_manager, db=db)
    bp_auth_register_parent.register_blueprint(bp_auth_login_view_child)
    app.register_blueprint(bp_auth_register_parent)
    
    from .projects_module import bp_project_view
    app.register_blueprint(bp_project_view)