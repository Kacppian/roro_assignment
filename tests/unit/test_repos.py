from project.repos import views
import pytest
import github

def test_generate_folder_slugs_with_heirarchy():
    slugs = views.generate_folder_slugs_with_heirarchy('/app/project/contents.py')
    assert slugs[0]['path'] == 'app'
    assert slugs[0]['name'] == 'app'

    assert slugs[1]['path'] == 'app/project'
    assert slugs[1]['name'] == 'project'

    assert slugs[2]['path'] == 'app/project/contents.py'
    assert slugs[2]['name'] == 'contents.py'

    slugs = views.generate_folder_slugs_with_heirarchy('/')
    assert len(slugs) == 0

    slugs = views.generate_folder_slugs_with_heirarchy('////')
    assert len(slugs) == 0

    slugs = views.generate_folder_slugs_with_heirarchy('//random/file/')
    assert slugs[0]['path'] == 'random'
    assert slugs[0]['name'] == 'random'

    assert slugs[1]['path'] == 'random/file'
    assert slugs[1]['name'] == 'file'

def test_generate_file_nav_urls():
    urls = views.generate_file_nav_urls(
                                        owner_name='kacppian',
                                        repo_name='roro_assignment',
                                        path='/',
                                        view_func='repos.get_dirs')
    assert urls == []

def test_syntax_highlight():
    test_content = 'laskdmsndadnian asda asdad'
    highlighted = views.syntax_highlight(test_content, None)
    assert type(highlighted) == str
    assert test_content in highlighted

    highlighted = views.syntax_highlight(test_content, 'somerandomfilename')
    assert type(highlighted) == str
    assert test_content in highlighted

def test_get_repo():
    repo = views.get_repo('kacppian', 'roro_assignment')
    assert repo.name.lower() == 'roro_assignment'
    assert repo.owner.login.lower() == 'kacppian'
    # This is strictly for entertainment purposes.
    # You can break this by uncommenting and watching the repo.. :p
    # assert repo.watchers_count == 0

    with pytest.raises(github.GithubException):
        repo = views.get_repo('kacppian', 'some_random_repo')

def test_get_contents():
    repo = views.get_repo('kacppian', 'roro_assignment')
    repo_contents = views.get_contents('/', repo)
    assert type(repo_contents) == list

    with pytest.raises(github.GithubException):
        repo_contents = views.get_contents('random_path', repo)

def test_contruct_path():
    test_path = views.contruct_path('/some/random/dir', None)
    assert test_path == '/some/random/dir'

    test_path = views.contruct_path(None, 'random_file_name')
    assert test_path == 'random_file_name'

    test_path = views.contruct_path('/some/random/dir', 'random_file_name')
    assert test_path == '/some/random/dir/random_file_name'

    test_path = views.contruct_path(None, None)
    assert test_path == '/'

def test_get_next_page_number():
    assert views.get_next_page_number(12) == 13
    assert views.get_next_page_number(-1) == 1
    assert views.get_next_page_number(0) == 1

def test_get_prev_page_number():
    assert views.get_prev_page_number(12) == 11
    assert views.get_prev_page_number(-1) == 0
    assert views.get_prev_page_number(0) == 0





