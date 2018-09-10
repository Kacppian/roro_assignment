from flask import Blueprint, request, render_template, url_for
from project import github_instance

home_blueprint = Blueprint(
                           'home',
                           __name__,
                           template_folder='./templates',
                           static_folder='./static',
                           static_url_path='home'
                           )

def get_popular_repos():
    repos = github_instance.search_repositories(
                                                'stars:>=40000',
                                                sort='stars',
                                                order='desc'
                                                )
    return repos.get_page(0)

def get_next_page_number(page_number):
    if page_number < 0:
      return 1
    return (page_number+1)

def get_prev_page_number(page_number):
    if page_number > 0:
        return (page_number - 1)
    return 0

def construct_pagination_urls(username, page_number):
    next_url = url_for(
                         'home.search_for_user',
                          username=username,
                         page=get_next_page_number(page_number)
                         )

    prev_url = url_for(
                         'home.search_for_user',
                          username=username,
                         page=get_prev_page_number(page_number)
                         )
    return (next_url, prev_url)

def search_users(query_string):
  users = github_instance.search_users(query_string, sort='followers')
  return users


@home_blueprint.route('/')
def home():
    popular_repos = get_popular_repos()
    return render_template('./home/index.html', popular_repos=popular_repos)

@home_blueprint.route('/search/<string:username>')
def search_for_user(username):
    page_number = request.args.get('page', 0, type=int)
    next_url, prev_url = construct_pagination_urls(username, page_number)
    users = search_users(username).get_page(page_number)
    return render_template('./home/search.html',
                           users=users,
                           next_url=next_url,
                           prev_url=prev_url
                           )

