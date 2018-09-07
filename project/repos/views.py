from flask import Blueprint, request, jsonify, session, render_template, redirect, Markup
from textile import textile
# from flask_login import current_user, login_user
from project import github_instance

repos_blueprint = Blueprint(
                           'repos',
                           __name__,
                           template_folder='./templates',
                           static_folder='./static'
                           )
repo_names = {}

@repos_blueprint.context_processor
def utility_processor():
    def convert_text_to_html(string):
        return textile(string)

    def get_fragment_list(path):
        path_fragment_list = list(filter(None, path.split('/')))[3:]
        urls = []
        for index in range(len(path_fragment_list)):
            url_path = '/'.join(path_fragment_list[:index+1])
            url_name = path_fragment_list[index]
            urls.append(dict(url_path=url_path, url_name=url_name))
        return urls

    return dict(
                convert_text_to_html=convert_text_to_html,
                get_fragment_list=get_fragment_list
                )


def get_repo(owner_name, repo_name):
    full_repo_name = "{}/{}".format(owner_name, repo_name)
    if repo_names.get(full_repo_name) is not None:
        return repo_names[full_repo_name]
    repo = github_instance.get_repo(full_repo_name)
    repo_names[full_repo_name] = repo
    return repo

def get_contents(path, repo):
    return repo.get_contents(path)

@repos_blueprint.route('/<owner_name>/<repo_name>/')
def get_repo_structure(owner_name, repo_name):
    # print('----------------')
    # print(owner_name)
    # print(repo_name)
    repo = get_repo(owner_name, repo_name)
    repo_contents = get_contents('/', repo)
    # print(repo_contents)
    # repo_content = get_repo_content(repo_name="{}/{}".format(owner_name, repo_name))
    return render_template('./repos/index.html', repo_contents=repo_contents, repo=repo)

@repos_blueprint.route('/<owner_name>/<repo_name>/<path:dir_name>/', defaults={'file_name': None})
@repos_blueprint.route('/<owner_name>/<repo_name>/<path:dir_name>/<file_name>')
def get_dir(owner_name, repo_name, dir_name, file_name=None):
    # print(file_name)
    # print(dir_name)
    if file_name:
        path = "{}/{}".format(dir_name, file_name)
    else:
        path = dir_name
    repo = get_repo(owner_name, repo_name)
    repo_contents = get_contents(path, repo)
    # print(repo_contents)
    return render_template('./repos/index.html', repo_contents=repo_contents, repo=repo)



# @repos_blueprint.route('/<owner_name>/<repo_name>/<path:dir_name>/<file_name>')
# def get_file(owner_name, repo_name, dir_name, file_name):
#     print('************8')
#     print(file_name)
#     repo = get_repo(owner_name, repo_name)
#     file_path = "{}/{}".format(dir_name, file_name)
#     file_content = get_contents(file_path, repo)
#     return render_template('./repos/file.html', file_content=file_content)



