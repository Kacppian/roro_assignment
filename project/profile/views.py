from flask import Blueprint, request, jsonify, session, render_template, redirect
# from flask_login import current_user, login_user
# from project.models import User
# from project import db
from project import github_instance

profile_blueprint = Blueprint('profile', __name__, template_folder='./templates')

def get_github_user(username):
    github_user = github_instance.get_user(username)
    return github_user

@profile_blueprint.route('/profile/<username>', methods=['GET'])
def profile(username):
    # user = User.query.filter_by(id=3).first_or_404()
    user = get_github_user(username)
    return render_template('./profile/show.html', user=user)




