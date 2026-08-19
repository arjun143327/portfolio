import sys
import os

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app import app as flask_app

def app(environ, start_response):
    # Vercel might rewrite PATH_INFO. We restore it from the raw request URI if possible.
    if 'REQUEST_URI' in environ:
        environ['PATH_INFO'] = environ['REQUEST_URI'].split('?')[0]
    
    # If PATH_INFO is still /api/index, the rewrite swallowed it. Let's fallback to checking HTTP_X_Vercel_Forwarded_Path
    # Actually, Flask handles REQUEST_URI itself if Werkzeug is used, but Vercel's python environment is plain WSGI.
    return flask_app(environ, start_response)
