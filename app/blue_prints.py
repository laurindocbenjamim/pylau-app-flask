

from app.auth_package.module_sign_up_sub.model.users import Users
from app.token_module import UserToken
from app.configs_package import csrf, jwt

from app.package_video_analytic.bp_video_analytic import bp_video_analytic
from app.api.auth.login_rest_api import login_rest_api_bp
from app.api.auth.register_rest_api import register_rest_api_bp
from app.api.auth.refresh_token_view import refresh_token_bp
from app.api.auth.user_profile_rest_api import user_profile_rest_api_bp
from app.api.auth.logout_rest_api import logout_rest_api_bp
#from ...utils import __get_cookies, set_header_params

def load_blueprints(app, db, login_manager, limiter):
    """

    """
    
    # Register the Blueprint
    login_rest_api_bp.register_blueprint(refresh_token_bp)
    login_rest_api_bp.register_blueprint(register_rest_api_bp)
    login_rest_api_bp.register_blueprint(user_profile_rest_api_bp)
    login_rest_api_bp.register_blueprint(logout_rest_api_bp)
    app.register_blueprint(login_rest_api_bp, url_prefix='/api-auth')

    # Exempt the Blueprint from CSRF protection
    csrf.exempt(login_rest_api_bp)

    # Integrating the sitemap 
    from app.utils.views.bp_sitemap import bp_sitemap
    app.register_blueprint(bp_sitemap)
    
    # Integrating the blueprints parent and child into the application
    #"""
    from app.auth_package import bp_auth_register_parent, init_register_app
    from app.auth_package import bp_auth as bp_auth_login_view_child, init_login_app
    init_register_app()
    init_login_app(login_manager=login_manager, db=db)

    #limiter.limit("10 per minute")(bp_auth_login_view_child)
    limiter.limit("10 per minute")(bp_auth_register_parent)

    bp_auth_register_parent.register_blueprint(bp_auth_login_view_child)
    app.register_blueprint(bp_auth_register_parent)
    #"""

    
    from app.email_module import bp_email_view
    app.register_blueprint(bp_email_view)
    
    from app.package_data_science.projects_module import bp_project_view
    app.register_blueprint(bp_project_view)

    from app.admin_module.bp_admin_view import bp as bp_admin_view
    from app.package_user.bp_user import bp_user
    
    limiter.limit("50 per minute")(bp_admin_view)

    bp_admin_view.register_blueprint(bp_user)
    app.register_blueprint(bp_admin_view)

    from app.test_forms.bp_form import bp as bp_form
    app.register_blueprint(bp_form)

    from app.web_scrappin_module.bp_web_scrapping_view import bp as bp_web_scrapping_view
    app.register_blueprint(bp_web_scrapping_view)

    from app.subscription_module import bp as bp_subscriber
    app.register_blueprint(bp_subscriber)

    #from ...package_data_science.bp_data_science_view import bp_data_science
    from app.package_data_science import bp_data_science
    app.register_blueprint(bp_data_science)

    #
    from app.api.netcaixa import bp_netcaixa
    app.register_blueprint(bp_netcaixa)

    # Importing the netcaixa package
    from app.api import bp_api
    app.register_blueprint(bp_api)

    #
    from app.package_prompts.bp_prompt_ai import bp_ai
    limiter.limit("100 per minute")(bp_ai)
    app.register_blueprint(bp_ai)


    # Importing the reports views
    from app.package_reports import bp_reports
    app.register_blueprint(bp_reports)


    # Importing the author route 
    from app.author_profile import bp_author
    app.register_blueprint(bp_author)

    # Importing the blueprint of articles
    from app.package_blog import bp_blog
    app.register_blueprint(bp_blog)

    # Importing the blueprint of courses
    from app.package_courses import bp_courses
    

    # Importing the blueprint of my learning 
    from app.package_learning import bp_learn
    from app.package_code_editor.bp_editor_view import bp_editor

    limiter.limit("60/hour")(bp_editor)

    bp_learn.register_blueprint(bp_editor)
    bp_courses.register_blueprint(bp_learn)   
     
    app.register_blueprint(bp_courses)

    # Importing the blueprint of the audit package
    from app.package_auditapp.bp_auditapp import bp_audit
    app.register_blueprint(bp_audit)

    # Importing the blueprint of the video analytic package
    app.register_blueprint(bp_video_analytic)