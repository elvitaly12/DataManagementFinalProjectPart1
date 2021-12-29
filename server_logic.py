from flask import Flask, redirect, url_for, abort, request, render_template
from flask import Response
import DatabaseLogic as DB
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



@app.route('/register', methods=['GET', 'POST'])
def register():
    user_name_inserted = ""
    # error = None
    # if request.method == 'GET':
    #     if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #         error = 'Invalid Credentials. Please try again.'
    #     else:
    #          return redirect(url_for('home'))
    #          return render_template('login.html', error=error)

    if request.method == 'GET':
       user_name_inserted = request.args['UserName']
       chat_id_of_typer =  request.args['ChatId']
       if  DB.getChat_idByUsername(user_name_inserted) != None:
           Response(' username already exists", status=500')
       else:
           try:
               DB.registerUser(user_name_inserted, chat_id_of_typer)
           except Exception:
               Response('Internal Server Error', status=500)
               print("fdfds")



    return Response(user_name_inserted +' registered', status=200)


@app.route('/unregister', methods=['GET', 'POST'])
def uregister():
    user_name_uninserted=""
    # error = None
    # if request.method == 'GET':
    #     if request.form['username'] != 'admin' or request.form['password'] != 'admin':
    #         error = 'Invalid Credentials. Please try again.'
    #     else:
    #          return redirect(url_for('home'))
    #          return render_template('login.html', error=error)

    if request.method == 'GET':
        user_name_uninserted = request.args['UserName']
        chat_id_of_typer = request.args['ChatId']
        if DB.getUsernameByChatID(chat_id_of_typer) !=user_name_uninserted:
            Response("cant unregister other username", status=500)
        else:
            try:
                DB.unregisterUser(user_name_uninserted)
            except Exception:
                Response('Internal Server Error', status=500)

    return Response(user_name_uninserted +' unregistered', status=200)






@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

