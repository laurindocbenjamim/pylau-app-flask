


def get_bp_components(app, db):
    
    from .authmodule.authmodule import two_factor_app_auth
    app.register_blueprint(two_factor_app_auth.bpapp)

    from . authmodule.codeskill import dictionaries
    app.register_blueprint(dictionaries.bpapp)

    from .authmodule import authrouter
    app.register_blueprint(authrouter.bpapp)

    from . authmodule.authmodule import two_factor_auth
    app.register_blueprint(two_factor_auth.bpapp)

    from . authmodule import userroutes
    app.register_blueprint(userroutes.bp)
    #from . authmodule.userroutes import run_routes
    
