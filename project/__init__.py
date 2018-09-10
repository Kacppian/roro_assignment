from flask import Flask, render_template
from github import Github
import os

github_instance = Github(os.environ.get('GITHUB_TOKEN'), per_page=50)

def error_handling(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('project/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('project/500.html'), 500

# Blueprints
def register_blueprints(app):
    from project.profile.views import profile_blueprint
    app.register_blueprint(profile_blueprint, url_prefix='/profile')

    from project.home.views import home_blueprint
    app.register_blueprint(home_blueprint, url_prefix='/')

    from project.repos.views import repos_blueprint
    app.register_blueprint(repos_blueprint, url_prefix='/repos')


def create_app(opts={}):
    app = Flask(__name__)
    app.config['DEVELOPMENT'] = True
    app.config['PROPAGATE_EXCEPTIONS'] = True
    for key in opts.keys():
        app.config[key] = opts[key]
    error_handling(app)
    register_blueprints(app)
    return app


