


def get_bp_components(app, db):
    
    from .maintenance_module import routes
    app.register_blueprint(routes.bp)
    from .authmodule import two_factor_app_auth_route
    app.register_blueprint(two_factor_app_auth_route.bp)

    from .authmodule import authrouter
    app.register_blueprint(authrouter.bp)

    from .authmodule import _two_factor_auth_route
    app.register_blueprint(_two_factor_auth_route.bp)
    #app.add_url_rule('/two_factor_auth', view_func=two_factor_auth.two_factor_auth, methods=['GET', 'POST'])    

    from . authmodule import userroutes
    app.register_blueprint(userroutes.bp)
    #from . authmodule.userroutes import run_routes

    from core.smtpmodule import send_email_routes
    app.register_blueprint(send_email_routes.bp)
    
