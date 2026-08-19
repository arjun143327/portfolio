import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app  # type: ignore

# Vercel serverless function entrypoint
# The WSGI app instance must be exposed as `app`
if __name__ == '__main__':
    app.run()
