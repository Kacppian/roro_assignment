from project.home import views
import pytest
import github
from flask import url_for

def test_construct_pagination_urls(test_client):
    username = 'kacppian'
    next_url, prev_url = views.construct_pagination_urls(username, 0)
    assert next_url == url_for(
                         'home.search_for_user',
                          username=username,
                          page=1
                         )

    assert prev_url == url_for(
                         'home.search_for_user',
                          username=username,
                          page=0
                         )

    next_url, prev_url = views.construct_pagination_urls(username, 1)
    assert next_url == url_for(
                         'home.search_for_user',
                          username=username,
                          page=2
                         )

    assert prev_url == url_for(
                         'home.search_for_user',
                          username=username,
                          page=0
                         )

    next_url, prev_url = views.construct_pagination_urls(username, -300)
    assert next_url == url_for(
                         'home.search_for_user',
                          username=username,
                          page=1
                         )

    assert prev_url == url_for(
                         'home.search_for_user',
                          username=username,
                          page=0
                         )

def test_home(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Maybe search for some users?" in response.data

def test_search_for_user(test_client):
    search_url = url_for(
                         'home.search_for_user',
                         username='kacppian'
                         )
    response = test_client.get(search_url)
    assert response.status_code == 200
    assert b"Users" in response.data
