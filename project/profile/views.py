from flask import Blueprint, request, render_template
from project import github_instance

profile_blueprint = Blueprint('profile', __name__, template_folder='./templates', static_folder='./static')

def get_github_user(username):
    github_user = github_instance.get_user(username)
    return github_user

@profile_blueprint.route('/<username>', methods=['GET'])
def profile(username):
    user = get_github_user(username)
    return render_template('./profile/index.html', user=user)




