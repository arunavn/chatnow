from flask.wrappers import Response
from flask_restful import Resource
from flask import jsonify, request, make_response, send_file, current_app
from requests.sessions import session
from webargs.flaskparser import use_args, use_kwargs
import os, io
from chatnow.utilities.auth import user_api_utils
from webargs import fields
from marshmallow import Schema, fields, validate
import json

class ProfilePic(Resource):
    @use_kwargs({'version': fields.Str()}, location= 'query')
    def get(self, id, **kwargs):
        response_content = user_api_utils.api_get_profilepic( id= id, version= kwargs.get("version", None) ).content
        resp= send_file(
            io.BytesIO(response_content),
            mimetype= 'application/octet-stream',
        )
        return resp
class Chats(Resource):
    @use_kwargs({'filterstring': fields.Str()}, location= 'query')
    def get(self, **kwargs):
        filterstring= kwargs.get('filterstring', None)
        resp=  user_api_utils.api_get_chats(filterstring= filterstring)
        if resp != False:
            return resp.json() , 200
        else:
            return [], 200
class People(Resource):
    @use_kwargs({'filterstring': fields.Str(required= True)}, location= 'query')
    def get(self, **kwargs):
        filterstring= kwargs.get('filterstring', None)
        resp= user_api_utils.api_get_people(filterstring)
        if resp != False:
            return resp.json() , 200
        else:
            return [], 200
class Messages(Resource):
    def post(self):
        messages = MessagePost( many=True).load(request.get_json())
        # messages = json.dumps(messages)
        res= user_api_utils.api_send_message(messages)
        if res:
            return 'Message sent', 201
        return 'Error in sending message', 400

    @use_kwargs({'otheruser': fields.Integer(required= True), 'frommsg': fields.Integer(), 'nprev': fields.Integer()}, location= 'query')        
    def get(self, **kwargs):
        message_list  = ( user_api_utils.api_get_messages(**kwargs) ).json()
        if message_list != False:
            return message_list, 200
        else:
            return [], 200

class MessagePost(Schema):
    sender= fields.Integer()
    reciever= fields.Integer(required=True)
    messagetype= fields.String(required=True)
    message= fields.String(required=True)




      
        