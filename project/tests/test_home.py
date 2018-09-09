import os
import unittest

from project import app
from .home.views import get_popular_repos


class BasicTests(unittest.TestCase):
    def setup(self):
        pass


    def teardown(self):
        pass


    def test_popular_repos(self):
        popular_repos_list = get_popular_repos()
        assert_equal()



if __name__ == "__main__":
    unittest.main()
