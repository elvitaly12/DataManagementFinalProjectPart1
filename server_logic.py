from flask import Flask, redirect, url_for, abort, request, render_template
from flask import Response
from werkzeug.debug import get_current_traceback

import logging

app = Flask(__name__)



@app.errorhandler(404)
def page_not_found(e):
    return '404 Not Found', 404


@app.errorhandler(500)
def internal_error(e):
    print(e)
    return "500 Error"


# Route for handling the login page logic
@app.route('/register', methods=['GET', 'POST'])
def register():
    # error = None
    # if request.method == 'GET':
    #     if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #         error = 'Invalid Credentials. Please try again.'
    #     else:
    #          return redirect(url_for('home'))
    #          return render_template('login.html', error=error)

    if request.method == 'GET':
       user_to_register = request.args['username']
       print("INSERT USER TO DB")
       return Response('OK', status=200)



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

