from project.repos import views
import pytest
import github
from flask import url_for

def test_generate_file_nav_urls(test_client):
    file_nav_urls = views.generate_file_nav_urls(
                                                 owner_name='kacppian',
                                                 repo_name='roro_assignment',
                                                 path='/',
                                                 view_func='repos.get_dirs'
                                                 )
    assert len(file_nav_urls) == 0

    file_nav_urls = views.generate_file_nav_urls(
                                                 owner_name='kacppian',
                                                 repo_name='roro_assignment',
                                                 path='random/dir',
                                                 view_func='repos.get_dirs'
                                                 )

    assert len(file_nav_urls) == 2
    assert file_nav_urls[0]['url_name'] == 'random'
    assert file_nav_urls[0]['url'] == "{}{}".format(
                                                    url_for(
                                                            'repos.get_dirs',
                                                            owner_name='kacppian',
                                                            repo_name='roro_assignment'
                                                            ),
                                                    'random'
                                                    )

    assert file_nav_urls[1]['url_name'] == 'dir'
    assert file_nav_urls[1]['url'] == "{}{}".format(
                                                    url_for(
                                                            'repos.get_dirs',
                                                             owner_name='kacppian',
                                                             repo_name='roro_assignment'
                                                            ),
                                                    'random/dir'
                                                    )

def test_get_dirs(test_client):
    repo_url = url_for(
                        'repos.get_dirs',
                        owner_name='kacppian',
                        repo_name='roro_assignment'
                      )
    response = test_client.get(repo_url)
    assert response.status_code == 200
    assert b"Pipfile" in response.data

def test_get_files(test_client):
    file_url = url_for(
                        'repos.get_file',
                        owner_name='kacppian',
                        repo_name='roro_assignment',
                        file_path='Pipfile'
                      )
    response = test_client.get(file_url)
    assert response.status_code == 200

def test_get_commits(test_client):
    commit_history_url = url_for(
                                 'repos.get_commits',
                                 owner_name='kacppian',
                                 repo_name='roro_assignment',
                                 path='Pipfile'
                                 )

    response = test_client.get(commit_history_url)
    assert response.status_code == 200
    assert b"Commits" in response.data

    commit_history_url = url_for(
                                 'repos.get_commits',
                                 owner_name='kacppian',
                                 repo_name='roro_assignment',
                                 path='random'
                                 )

    response = test_client.get(commit_history_url)
    assert response.status_code == 200
    print(response.data)
    assert b"Sorry, there's no content here!" in response.data
