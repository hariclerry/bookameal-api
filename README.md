[![Build Status](https://travis-ci.org/RrNn/bookameal-api.svg?branch=ft-flask-api-swagg-docs-157273805)](https://travis-ci.org/RrNn/bookameal-api)
[![Coverage Status](https://coveralls.io/repos/github/RrNn/bookameal-api/badge.svg?branch=ft-flask-api-swagg-docs-157273805)](https://coveralls.io/github/RrNn/bookameal-api?branch=ft-flask-api-swagg-docs-157273805)
<a href="https://codeclimate.com/github/RrNn/bookameal-api/maintainability"><img src="https://api.codeclimate.com/v1/badges/2b0ccd6826ba1410d693/maintainability" /></a>


### bookameal
#### Application usage
* Bookameal is an application that allows users to register/create accouts, signin and view orders of meals from different days' menus available.
* Bookameal also allows caterers, or more clearly administrators to create accounts and create meal options from which they later choose menus for specific days.. and its those menus from which customers(other users) will choose a meal to order.

* To start using the app, clone it to your computer, like this;
* Click on the green button, with **Clone or download** and copy the link that shows.
* Open your terminal and write, `git clone <the link you have copied above>`
* `cd bookameal-api`
* `export FLASK_APP=bookameal`
* `export FLASK_DEBUG=1`
* `. venv\bin\activate`, this activates the virtual environment in order to find flask
* `flask run`
* After these the application will be served on your localhost at port `5000`

* To run the tests, cd to the application, activate the virtual environment and run pytest like, `pytest`
* Or if you want to see the coverage while testing, run `nosetests --with-coverage`

* A working demo can be found at https://rrnn.github.io/bookameal/
* To interact with the documentation, visit the hosted app on heroku at 
	https://book-a-good-meal.herokuapp.com/apidocs/