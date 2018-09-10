from project.profile import views
import pytest
import github
from flask import url_for

def test_get_details(test_client):
    user_details_url = url_for(
                               'profile.get_details',
                               username='kacppian'
                               )
    response = test_client.get(user_details_url)
    assert response.status_code == 200
    assert b"Public Repositories" in response.data
