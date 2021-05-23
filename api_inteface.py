from flask import Blueprint
from flask_restful import Api
from chatnow.utilities.api_interface.api_interface_resources import ProfilePic, Chats, People, Messages
api_bp= Blueprint('api_interface', __name__ , url_prefix= '/api' )

api= Api(api_bp)

api.add_resource(ProfilePic, '/profilepic/<string:id>')
api.add_resource(Chats, '/chats')
api.add_resource(People, '/people')
api.add_resource(Messages, '/messages')
