from flask import Flask
from flask_bootstrap import Bootstrap
from github import Github
import os

app = Flask(__name__)
app.config['GITHUB_CLIENT_ID'] = 'Iv1.7265011a9f876ab6'
app.config['GITHUB_CLIENT_SECRET'] = '5032c975fb5abbe46e0e1239c4a1b33da77e550c'
app.config['DEVELOPMENT'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.url_map.strict_slashes = True


# Bootstrap(app)
github_instance = Github('aade3a843efa808800c4f67964ad9c47b808977f', per_page=50)

# Blueprints
from project.profile.views import profile_blueprint
app.register_blueprint(profile_blueprint, url_prefix='/profile')

from project.home.views import home_blueprint
app.register_blueprint(home_blueprint, url_prefix='/')

from project.repos.views import repos_blueprint
app.register_blueprint(repos_blueprint, url_prefix='/repos')

