from flask import Flask

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)


fantasticsearch = Flask(__name__)
fantasticsearch.wsgi_app = ReverseProxied(fantasticsearch.wsgi_app)

# Load configurations
import json
with open('fantasticsearch/configs.json') as f:
        config = json.load(f)

from fantasticsearch import views
