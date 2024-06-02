


def get_bp_components(app, db):
    
    from .authmodule.authmodule import two_factor_app_auth
    app.register_blueprint(two_factor_app_auth.bp)

    from . authmodule.codeskill import dictionaries
    app.register_blueprint(dictionaries.bp)

    from .authmodule import authrouter
    app.register_blueprint(authrouter.bp)

    from . authmodule.authmodule import two_factor_auth
    app.register_blueprint(two_factor_auth.bp)
    #app.add_url_rule('/two_factor_auth', view_func=two_factor_auth.two_factor_auth, methods=['GET', 'POST'])    

    from . authmodule import userroutes
    app.register_blueprint(userroutes.bp)
    #from . authmodule.userroutes import run_routes
    
