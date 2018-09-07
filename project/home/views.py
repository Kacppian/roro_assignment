from flask import Blueprint, request, jsonify, session, render_template, redirect
# from flask_login import current_user, login_user
from project import github_instance

home_blueprint = Blueprint(
                           'home',
                           __name__,
                           template_folder='./templates',
                           static_folder='./static'
                           )

def get_popular_repos():
    repos = github_instance.search_repositories(
                                                'stars:>=40000',
                                                sort='stars',
                                                order='desc'
                                                )
    return repos.get_page(0)


@home_blueprint.route('/')
def home():
    repos = get_popular_repos()
    return render_template('./home/index.html', repos=repos)


