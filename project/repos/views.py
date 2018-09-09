from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from pygments.lexers import get_lexer_for_filename, special
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from pygments import highlight
from project import github_instance
from datetime import datetime
import arrow

repos_blueprint = Blueprint(
                           'repos',
                           __name__,
                           template_folder='./templates',
                           static_folder='./static'
                           )
# Needs to be cache
repo_names = {}

def generate_folder_slugs_with_heirarchy(path):
    slugs = path.split('/')
    heirarchical_slugs = []

    for slug_index in range(len(slugs)):
        path = '/'.join(slugs[:slug_index+1])
        name = slugs[slug_index]
        heirarchical_slugs.append(dict(
                                  name=name,
                                  path=path
                                  ))
    return heirarchical_slugs


def generate_file_nav_urls(owner_name, repo_name, path, base_api):

    if path == '/':
        return []
    base_repo_url = url_for(base_api, owner_name=owner_name, repo_name=repo_name)
    slugs = list(filter(None, generate_folder_slugs_with_heirarchy(path)))
    print(base_repo_url)
    print(slugs)
    generated_urls = []
    for slug in slugs:
        url = "{}{}".format(
                             base_repo_url,
                             slug['path']
                             )
        url_name = slug['name']
        generated_urls.append(dict(url=url, url_name=url_name))
    print(generated_urls)
    return generated_urls


def syntax_highlight(content, file_name=None):
    try:
        lexer = get_lexer_for_filename(file_name)
    except Exception as e:
        lexer = special.TextLexer()

    style = get_style_by_name('friendly')
    formatter = HtmlFormatter(linenos=True, style=style, noclasses=True)

    return highlight(content, lexer, formatter)

def get_repo(owner_name, repo_name):
    full_repo_name = "{}/{}".format(owner_name, repo_name)

    if repo_names.get(full_repo_name) is not None:
        return repo_names[full_repo_name]
    repo = github_instance.get_repo(full_repo_name)
    repo_names[full_repo_name] = repo

    return repo

def get_contents(path, repo):
    return repo.get_contents(path)

def contruct_path(dir_name, file_name):
    if file_name:
        path = "{}/{}".format(dir_name, file_name)
    elif dir_name:
        path = dir_name
    else:
        path = '/'

    return path

def get_next_page_number(page_number):
    return (page_number+1)

def get_prev_page_number(page_number):
    if page_number > 0:
        return (page_number - 1)
    return 0

def construct_pagination_urls(owner_name, repo_name, file_path, page_number):
    next_url = url_for(
                         'repos.get_commits',
                         owner_name=owner_name,
                         repo_name=repo_name,
                         path=file_path,
                         page=get_next_page_number(page_number)
                         )

    prev_url = url_for(
                         'repos.get_commits',
                         owner_name=owner_name,
                         repo_name=repo_name,
                         path=file_path,
                         page=get_prev_page_number(page_number)
                         )
    return (next_url, prev_url)

@repos_blueprint.route('/<owner_name>/<repo_name>/commits/master/')
@repos_blueprint.route('/<owner_name>/<repo_name>/commits/master/<path:path>/')
def get_commits(owner_name, repo_name, path='/'):
    repo = get_repo(owner_name, repo_name)
    # path = contruct_path(dir_name, file_name)
    page_number = request.args.get('page', 0, type=int)
    commits = repo.get_commits(path=path).get_page(page_number)
    file_nav_urls = generate_file_nav_urls(owner_name, repo_name, path, 'repos.get_commits')
    next_url, prev_url = construct_pagination_urls(
                                                   owner_name,
                                                   repo_name,
                                                   path,
                                                   page_number
                                                   )

    return render_template('./repos/commit_history.html',
                           commits=commits,
                           next_url=next_url,
                           prev_url=prev_url,
                           file_nav_urls=file_nav_urls,
                           repo=repo
                           )



@repos_blueprint.route('/<owner_name>/<repo_name>/tree/master/')
@repos_blueprint.route('/<owner_name>/<repo_name>/tree/master/<path:dir_name>/')
def get_dirs(owner_name, repo_name, dir_name=None):
    path = contruct_path(dir_name, None)
    repo = get_repo(owner_name, repo_name)
    repo_contents = get_contents(path, repo)
    file_nav_urls = generate_file_nav_urls(owner_name, repo_name, path, 'repos.get_dirs')
    history_url = url_for(
                          'repos.get_commits',
                          owner_name=owner_name,
                          repo_name=repo_name,
                          path=dir_name
                          )

    return render_template('./repos/index.html',
                           repo=repo,
                           file_nav_urls=file_nav_urls,
                           repo_contents=repo_contents,
                           history_url=history_url
                           )

@repos_blueprint.route('/<owner_name>/<repo_name>/blob/master/<path:file_path>')
def get_file(owner_name, repo_name, file_path):
    repo = get_repo(owner_name, repo_name)
    repo_contents = get_contents(file_path, repo)
    file_nav_urls = generate_file_nav_urls(owner_name,
                                           repo_name,
                                           file_path,
                                           'repos.get_dirs'
                                           )
    file_contents = syntax_highlight(
                                    repo_contents.decoded_content.decode('utf-8'),
                                    file_name=repo_contents.path
                                    )
    history_url = url_for(
                          'repos.get_commits',
                          owner_name=owner_name,
                          repo_name=repo_name,
                          path=file_path
                          )

    return render_template('./repos/index.html',
                           repo=repo,
                           file_nav_urls=file_nav_urls,
                           file_contents=file_contents,
                           history_url=history_url
                           )

