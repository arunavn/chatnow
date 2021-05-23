from flask import (
    Flask, render_template
    )
import os
from flask_bootstrap import Bootstrap


def create_app(test_config=None):
    app= Flask(__name__)
    Bootstrap(app)
    app.config['SECRET_KEY']='LongAndRandomSecretKey'
    app.config['UPLOAD_FOLDER'] = "uploads"
    if test_config is None:
        app.config.from_pyfile('config.py', silent= True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.mkdir(app.instance_path)
    except:
        pass
    try:
        os.mkdir('uploads')
    except:
        pass
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error.html', ecode='404', emsg= 'not found' ),404
    from chatnow.utilities.auth import user_api_utils

    @app.route('/hello')
    def hello():
        return user_api_utils.api_get_user()
    
 
    @app.after_request
    def add_cokies(response):
        response.set_cookie('api_base_url', (os.environ).get('API_BASE_URL', ''))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'X-CSRF-TOKEN,Content-Type,Access-Control-Allow-Origin'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'POST,PATCH,GET,DELETE'
        return response
    from . import auth, chat, api_inteface
    app.register_blueprint(auth.bp)
    
    app.register_blueprint(chat.bp)
    app.add_url_rule('/', endpoint= 'chats')
    app.register_blueprint(api_inteface.api_bp)
    return app
