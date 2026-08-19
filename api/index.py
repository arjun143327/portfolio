import sys
import os
from urllib.parse import parse_qs

# Link the backend directory
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Now we can import the Flask app
from app import app as flask_app

def app(environ, start_response):
    """
    Vercel WSGI Wrapper.
    Restores the PATH_INFO from the Vercel routing query parameter.
    """
    query_string = environ.get('QUERY_STRING', '')
    query_params = parse_qs(query_string)
    
    if 'vercel_path' in query_params:
        # Restore the original path so Flask routing works correctly
        environ['PATH_INFO'] = '/api/' + query_params['vercel_path'][0]
        
    return flask_app(environ, start_response)
