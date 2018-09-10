from project.profile import views
import pytest
import github

def test_get_github_user():
    github_user = views.get_github_user('kacppian')
    assert github_user.login.lower() == 'kacppian'
    assert github_user.name.lower() == 'kaushik asp'

    with pytest.raises(github.GithubException):
        github_user = views.get_github_user('some random name')



