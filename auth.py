from flask import (
    Blueprint, render_template, request, redirect, url_for, make_response, session
)
from . import wtForms
from chatnow.utilities.auth import user_api_utils
from flask import flash, send_file
import os
import urllib.parse
bp= Blueprint('auth', __name__, url_prefix= '/auth')

import functools
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('chatnow_id', None) is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/register', methods= ['POST', 'GET'])
def register():
    #api_base_url = "http://127.0.0.1:5000"
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    form = wtForms.RegisterForm(request.form)
    if request.method == 'POST':
        if  form.validate() and user_api_utils.api_register_user(request.form):
            flash( "Registration successfull, credentials sent to {}".format((request.form).get('email') ), 'info' )
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form, page= 'register', api_base_url= api_base_url)

@bp.route('/login', methods= ['POST', 'GET'])
def login():
    #api_base_url = "http://127.0.0.1:5000"
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    api_domain_url = api_base_url.split('://')[1]
    print(api_base_url)
    form= wtForms.LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        login_status= user_api_utils.api_login(request.form['userid'], request.form['password'])
        if login_status:
            session['chatnow_userid']=  request.form['userid']
            resp= make_response(redirect(url_for('auth.confirmLogin')))
            resp.set_cookie('access_token_cookie', login_status.cookies['access_token_cookie'])
            resp.set_cookie('csrf_access_token', login_status.cookies['csrf_access_token'])
            return resp
    return render_template('auth/login.html', form= form, page= 'login', api_base_url= api_base_url)

@bp.route('/confirmlogin')
def confirmLogin():
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    app_base_url = os.environ.get('APP_BASE_URL', ' ')
    userid= session.get('chatnow_userid', None)
    if userid is not None:
        logged_in_user= user_api_utils.api_search_user(userid)
        if logged_in_user is not None:
            session['chatnow_id']= logged_in_user.get('id', None)
    
    return redirect(url_for('chats'))

@bp.route('/logout')
def logout():
    session['chatnow_id']= None
    session['chatnow_userid']= None
    response= make_response(redirect(url_for('auth.confirmLogout')))

#    api_cookies= [
#     { name: 'access_token_cookie', 'value': '', 'expires': 0 },
#     { name: 'access_token_cookie', 'value': '', 'expires': 0 }
#    ]
#    api_set_cookies(response, api_cookies)
    response.set_cookie('access_token_cookie', '', expires=0)
    response.set_cookie('csrf_access_token', '', expires=0)
    return response

@bp.route('/confirmlogout')
def confirmLogout():
    flash( "Logout successfull", 'success' )         
    return redirect(url_for('auth.login'))

@bp.route('/troubleinlogin', methods= ['GET', 'POST'])
def troubleInLogin():
    #api_base_url = "http://127.0.0.1:5000"
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    form= wtForms.TroubleInLogin(request.form)
    if request.method == 'POST' and form.validate():
        if (request.form).get('trouble', None) == 'P' and user_api_utils.api_forgot_password(request.form):
            flash( "Password reset successful, credentials sent to {}".format((request.form).get('email') ), 'success' )
            return redirect(url_for('auth.login'))
        if (request.form).get('trouble', None) == 'U' and user_api_utils.api_forgot_userid((request.form).get('email', None)):
            flash( "Userid sent to {}".format((request.form).get('email') ), 'success' )
            return redirect(url_for('auth.login'))
    return render_template('auth/troubleinlogin.html', form= form, page= 'trouble', api_base_url= api_base_url)

@bp.route('/profilepic/<string:id>')
def send_profilepic(id):
    x= user_api_utils.api_get_profilepic(id)
    response = send_file(
                x.content
                )
    return response


