from project.home import views
import pytest
import github

def test_get_next_page_number():
    assert views.get_next_page_number(12) == 13
    assert views.get_next_page_number(-1) == 1
    assert views.get_next_page_number(0) == 1

def test_get_prev_page_number():
    assert views.get_prev_page_number(12) == 11
    assert views.get_prev_page_number(-1) == 0
    assert views.get_prev_page_number(0) == 0

def test_get_popular_repos():
    repos = views.get_popular_repos()
    assert len(repos) <= 50

def test_search_users():
    searched_users = views.search_users('kacppian')
    assert type(searched_users.get_page(0)) is list
    assert len(searched_users.get_page(0)) <= 50

    with pytest.raises(AssertionError):
        searched_users = views.search_users('')
