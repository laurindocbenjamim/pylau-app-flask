


def get_bp_components(app, db):
    
    from .modules.authmodule import two_factor_app_auth
    app.register_blueprint(two_factor_app_auth.bpapp)

    from . modules.codeskill import dictionaries
    app.register_blueprint(dictionaries.bpapp)

    from .modules.authmodule import authcontroller
    app.register_blueprint(authcontroller.bpapp)

    from . modules.authmodule import two_factor_auth
    app.register_blueprint(two_factor_auth.bpapp)
