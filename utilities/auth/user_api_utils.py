import requests
import os
from flask import session,request, make_response, jsonify, current_app
#url= "http://127.0.0.1:5000/accounts/user/bob12"
#headers= {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTYxNzkxMDM2OSwianRpIjoiMzRjYzdhMDgtMGQ5Ni00ZjQyLTg1MjQtZjllZDBlZTI0MjZhIiwibmJmIjoxNjE3OTEwMzY5LCJ0eXBlIjoiYWNjZXNzIiwic3ViIjoiMSIsImV4cCI6MTYxNzkxMTI2OX0.9wdknniqqALI2D_QoCKxLVHfyNK83KrAB-AX-0DpwKo'}
#response = requests.get(url, headers=headers)
#print((response.json()))
def api_login(userid, password):
    api_base_url = "http://127.0.0.1:5000"
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    url=  api_base_url + "/accounts/login"
    json= {'userid': userid, 'password': password }
    response = requests.post(url, json=json)
    if (response.status_code== 200):
        return response
    else:
        return False
def api_search_user(value, findby= None, token= True):
    if findby is None:
        findby= 'userid'
    csrf_token= request.cookies.get('csrf_access_token', None)
    access_token= request.cookies.get('access_token_cookie', None) 
    headers, cookies= {}, {}
    if csrf_token is not None and token:
        headers= {'X-CSRF-TOKEN': csrf_token}
    if access_token is not None and token:
        cookies = { 'access_token_cookie': access_token }
    api_base_url = "http://127.0.0.1:5000"
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    url=  api_base_url + "/accounts/user/{}/{}".format(findby, value)
    response = requests.get(url, headers= headers, cookies= cookies)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def api_register_user(userdata):
    json= {
            "id": "",
            "userid": "",
            "email": "",
            "name": "",
            "password": "",
            "about": ""
        }
    json= { key: userdata.get(key, '') for key,value in json.items()  }
    api_base_url = "http://127.0.0.1:5000"
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    url=  api_base_url + "/accounts/user"
    response = requests.post(url, json=json)
    if response.status_code == 201:
        return True
    return False
def api_get_user():
    api_base_url = "http://127.0.0.1:5000"
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    url=  api_base_url + "/accounts/users"
    headers= {'X-CSRF-TOKEN': request.cookies.get('csrf_access_token')}
    cookies = { 'access_token_cookie': request.cookies.get('access_token_cookie') }
    response = requests.get(url, headers=headers, cookies= cookies)
    return response.text

def api_set_cookies(response, api_cookies= None):
    if api_cookies is not None:
        for c in api_cookies:
            response.set_cookie(c.get('name', None), c.get('value', None) , expires= c.get('expires', 0))



def api_forgot_password(userdata):
    json= {
            "id": "",
            "userid": "",
            "email": "",
            "name": "",
            "password": "",
            "about": ""
        }
    json= { key: userdata.get(key, '') for key,value in json.items()  }
    api_base_url = "http://127.0.0.1:5000"
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    url=  api_base_url + "/accounts/user/email/{}/forgotpassword".format(json.get('email', ''))
    response = requests.patch(url, json=json)
    if response.status_code == 200:
        return True
    return False
def api_forgot_userid(email):
    findby= 'email'
    api_base_url = "http://127.0.0.1:5000"
    url=  api_base_url + "/accounts/user/email/{}/forgotuserid".format(email)
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False

def api_get_profilepic(id, version=None):
    api_base_url = "http://127.0.0.1:5000"
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    url=  api_base_url + "/accounts/profilepic/{}".format(id)
    if version is not None:
        url = url + '?version=' + version
    headers= {'X-CSRF-TOKEN': request.cookies.get('csrf_access_token')}
    cookies = { 'access_token_cookie': request.cookies.get('access_token_cookie') }
    response = requests.get(url, headers=headers, cookies= cookies)
    if response.status_code == 200:
        return response
    else:
        return False
def api_get_chats(filterstring= None):
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    if filterstring is not None:
        url=  api_base_url + "/chats?filterstring=" + filterstring
    else:
        url=  api_base_url + "/chats"
    headers= {'X-CSRF-TOKEN': request.cookies.get('csrf_access_token')}
    cookies = { 'access_token_cookie': request.cookies.get('access_token_cookie') }
    response = requests.get(url, headers=headers, cookies= cookies)
    if response.status_code == 200:
        return response
    else:
        return False
def api_get_people(filterstring= None):
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    if filterstring is not None:
        url=  api_base_url + "/people?filterstring=" + filterstring
    headers= {'X-CSRF-TOKEN': request.cookies.get('csrf_access_token')}
    cookies = { 'access_token_cookie': request.cookies.get('access_token_cookie') }
    response = requests.get(url, headers=headers, cookies= cookies)
    if response.status_code == 200:
        return response
    else:
        return False
def api_send_message(messages):
    json= messages
    api_base_url = "http://127.0.0.1:5000"
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    url=  api_base_url + "/messages"
    headers= {'X-CSRF-TOKEN': request.cookies.get('csrf_access_token')}
    cookies = { 'access_token_cookie': request.cookies.get('access_token_cookie') }
    response = requests.post(url, json=json, headers=headers, cookies= cookies)
    if response.status_code == 200:
        return True
    return False

def api_get_messages(**kwargs):
    api_base_url = os.environ.get('API_BASE_URL', ' ')
    otheruser, nprev, frommsg = kwargs.get('otheruser', None), kwargs.get('nprev', None), kwargs.get('frommsg', None)
    url= api_base_url + '/messages?otheruser='+ str(otheruser)
    if nprev is not None:
        url+= '&nprev=' + str(nprev)
    if frommsg is not None:
        url+= '&frommsg=' + str(frommsg)
    headers= {'X-CSRF-TOKEN': request.cookies.get('csrf_access_token')}
    cookies = { 'access_token_cookie': request.cookies.get('access_token_cookie') }
    response = requests.get(url, headers=headers, cookies= cookies)
    if response.status_code == 200:
        return response
    else:
        return False




    
    

