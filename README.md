[![Build Status](https://travis-ci.org/RrNn/bookameal-api.svg?branch=flask-api-%23157243446)](https://travis-ci.org/RrNn/bookameal-api)
[![Coverage Status](https://coveralls.io/repos/github/RrNn/bookameal-api/badge.svg?branch=flask-api-%23157243446)](https://coveralls.io/github/RrNn/bookameal-api?branch=flask-api-%23157243446)


### bookameal
#### Application usage
* Bookameal is an application that allows users to register/create accouts, signin and view orders of meals from different days' menus available.
* Bookameal also allows caterers, or more clearly administrators to create accounts and create meal options from which they later choose menus for specific days.. and its those menus from which customers(other users) will choose a meal to order.

* To start usong the app, clone it to your local host, and then type the following commands in the terminal
* `cd bookameal`
* `export FLASK_APP=bookameal`
* `export FLASK_DEBUG=1`
* `. venv\bin\activate`, this activates the virtual environment in order to find flask
* `flask run`
* After these the application will be served on your localhost at port `5000`

* To run the tests, cd to the application, activate the virtual environment and run pytest like, `pytest`
* A working demo can be found at https://rrnn.github.io/bookameal/