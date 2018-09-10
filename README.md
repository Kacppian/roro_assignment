# Rorodata Assignment

## The Following Application was built on Flask

Please run the following steps to run it locally *or* visit it here - https://roro-assignment.herokuapp.com/

* `cd roro_assignment`
* `pipenv install`
* `export GITHUB_KEY='xxxxYOURxxxTOKEN'`
* `gunicorn --bind 0.0.0.0:8000 "app:create_app()"`

Voila, it should be running on localhost:8000

You can run the tests using in the root dir

`pytest`
