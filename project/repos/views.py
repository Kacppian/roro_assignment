from flask import Blueprint, request, jsonify, session, render_template, redirect
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from pygments.styles import get_style_by_name
from pygments import highlight
from project import github_instance

repos_blueprint = Blueprint(
                           'repos',
                           __name__,
                           template_folder='./templates',
                           static_folder='./static'
                           )
repo_names = {}

def color_it(file_name, content):
    lexer = get_lexer_for_filename(file_name)
    style = get_style_by_name('friendly')
    formatter = HtmlFormatter(linenos=True, style=style, noclasses=True)
    return highlight(content, lexer, formatter)

@repos_blueprint.context_processor
def utility_processor():
    def convert_text_to_html(file_name, content):
        # return textile(string)
        return color_it(file_name, content)

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
@repos_blueprint.route('/<owner_name>/<repo_name>/<path:dir_name>/')
@repos_blueprint.route('/<owner_name>/<repo_name>/<path:dir_name>/<file_name>')
def get_dir_or_file(owner_name, repo_name, dir_name=None, file_name=None):
    if file_name:
        path = "{}/{}".format(dir_name, file_name)
    elif dir_name:
        path = dir_name
    else:
        path = '/'

    repo = get_repo(owner_name, repo_name)
    repo_contents = get_contents(path, repo)
    return render_template('./repos/index.html', repo_contents=repo_contents, repo=repo)



