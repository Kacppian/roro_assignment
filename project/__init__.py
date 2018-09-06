from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_github import GitHub
from flask_bootstrap import Bootstrap
from github import Github
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kaushik:postgres@localhost/roro'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['GITHUB_CLIENT_ID'] = 'Iv1.7265011a9f876ab6'
app.config['GITHUB_CLIENT_SECRET'] = '5032c975fb5abbe46e0e1239c4a1b33da77e550c'
app.config['WTF_CSRF_SECRET_KEY'] = 'a csrf secret key'
app.config['SECRET_KEY'] = 'a secret key'
app.config['DEVELOPMENT'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
# app.url_map.strict_slashes = False

db = SQLAlchemy(app)
# login_manager = LoginManager(app)
Bootstrap(app)
github_instance = Github('aade3a843efa808800c4f67964ad9c47b808977f', per_page=30)

# Blueprints
# from project.auth.views import auth_blueprint
# from project.profile.views import profile_blueprint

# app.register_blueprint(auth_blueprint, url_prefix='/auth')
# app.register_blueprint(profile_blueprint, url_prefix='/user')
from project.home.views import home_blueprint
app.register_blueprint(home_blueprint)

from project.repos.views import repos_blueprint
app.register_blueprint(repos_blueprint, url_prefix='/repos')
# @app.route('/')
# def home():
#     return 'This home bitch!'

