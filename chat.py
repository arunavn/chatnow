from flask import Blueprint, render_template, session, request, flash, url_for
from werkzeug.utils import redirect
from chatnow.utilities.auth import user_api_utils
from chatnow.auth import login_required
from . import wtForms
import os

bp= Blueprint('chat', __name__ )


@bp.route('/')
@login_required
def chats():
    #api_base_url = "http://127.0.0.1:5000"
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    id= session.get('chatnow_id', None)
    name= 'user'
    user= None
    if id is not None:
        user= user_api_utils.api_search_user(findby= 'id', value= id)
        if user is not None:
            name= user.get('name', 'user')
    return render_template('chat/chats.html', name= name, page= 'chats', user_data= user, api_base_url= api_base_url )

@bp.route('/details/<string:foruser>')
@login_required
def details(foruser):
    #api_base_url = "http://127.0.0.1:5000"
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    id= session.get('chatnow_id', None)
    mode= 'others'
    user= None
    if id is not None:
        if int(foruser) == int(id):
            mode= 'self'
        user= user_api_utils.api_search_user(findby= 'id', value= foruser)
        if user is not None:
            name= user.get('name', 'user')
    return render_template('chat/details.html', page= 'details', mode= mode, user_data= user, api_base_url= api_base_url)

@bp.route('/settings')
@login_required
def settings():
    id= session.get('chatnow_id', None)
    user= None
    name= 'user'
    if id is not None:
        user= user_api_utils.api_search_user(findby= 'id', value= id)
        if user is not None:
            name= user.get('name', 'user')
    return render_template('chat/settings.html', page= 'settings', user_data=user )

@bp.route('/message/<string:touser>')
@login_required
def message(touser):
    #api_base_url = "http://127.0.0.1:5000"
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    id= session.get('chatnow_id', None)
    user= None
    name= 'user'
    if id is not None:
        print(id)
        print(touser)
        if int(id) == int(touser):
            print('x')
            return redirect('/')
        user= user_api_utils.api_search_user(findby= 'id', value= id)
        touser= user_api_utils.api_search_user(findby= 'id', value= touser)
        if user is not None:
            name= user.get('name', 'user')
    return render_template('chat/message.html', page= 'message', touser= touser, user_data=user, api_base_url= api_base_url )

@bp.route('/findpeople/<string:filterstring>')
@login_required
def findpeople(filterstring):
    id= session.get('chatnow_id', None)
    user= None
    name= 'user'
    if id is not None:
        user= user_api_utils.api_search_user(findby= 'id', value= id)
        if user is not None:
            name= user.get('name', 'user')
    return render_template('chat/find_people.html', page= 'findpeople', user_data=user)



@bp.route('/accountoptions/<string:func>', methods= ['POST', 'GET'])
@login_required
def accountoptions(func):
    #api_base_url = "http://127.0.0.1:5000"
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    if func == 'changeemail':
        form = wtForms.UpdateEmail(request.form)
    elif func == 'changepass':
        form = wtForms.UpdatePassword(request.form)
    else:
        form = wtForms.UpdatePersonalDetails(request.form)
    print(func)
    if request.method == 'POST':
        if  form.validate() and user_api_utils.api_register_user(request.form):
            flash( "Registration successfull, credentials sent to {}".format((request.form).get('email') ), 'info' )
            return redirect(url_for('auth.login'))
    return render_template('chat/accountupdate.html', form=form, page= 'Update', func= func, api_base_url= api_base_url )