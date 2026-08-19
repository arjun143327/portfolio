import os
import re
import pymysql
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

from db import db, Project, ContactMessage

load_dotenv()

# Basic validation setup
def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# Retrieve DB credentials
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_USER = os.environ.get("DB_USER", "root")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
DB_NAME = os.environ.get("DB_NAME", "portfolio_db")
DB_PORT = os.environ.get("DB_PORT", "3306")

# Detect if using a remote cloud DB (e.g. Aiven, TiDB, Railway)
is_cloud_db = DB_HOST not in ["localhost", "127.0.0.1", ""]

# 1. Automatically create the database if it doesn't exist
try:
    connect_kwargs = {
        "host": DB_HOST,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "port": int(DB_PORT)
    }
    if is_cloud_db:
        connect_kwargs["ssl"] = {"check_hostname": False}
        
    conn = pymysql.connect(**connect_kwargs)
    with conn.cursor() as cursor:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
    conn.commit()
    conn.close()
    print(f"Verified database '{DB_NAME}' exists.")
except Exception as e:
    print(f"Notice during DB pre-check: {e}")

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# 2. Configure Flask-SQLAlchemy with SSL support for cloud
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if is_cloud_db:
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "connect_args": {
            "ssl": {
                "check_hostname": False
            }
        }
    }

db.init_app(app)

# Fallback seed data in case cloud DB is initializing
FALLBACK_PROJECTS = [
    {
        "id": 1,
        "title": "Budgetrix",
        "description": "Comprehensive expense tracking and financial modeling platform with real-time data visualization.",
        "tech_stack": ["flutter", "riverpod"],
        "demo_url": "#",
        "repo_url": "#",
        "display_order": 1
    },
    {
        "id": 2,
        "title": "Grocery Dashboard",
        "description": "Automated financial reporting and inventory tracking system built for NGO logistics.",
        "tech_stack": ["Python", "Flask", "Excel API"],
        "demo_url": "#",
        "repo_url": "#",
        "display_order": 2
    },
    {
        "id": 3,
        "title": "Silent Bridge",
        "description": "Real-time ISL voice translation interface utilizing Web Speech API and animated avatars.",
        "tech_stack": ["JavaScript", "Web Speech", "WebGL"],
        "demo_url": "#",
        "repo_url": "#",
        "display_order": 3
    }
]

# 3. Create tables and automatically seed the database on startup
with app.app_context():
    try:
        db.create_all()
        
        # Seed projects if the table is currently empty
        if Project.query.count() == 0:
            print("Seeding initial projects...")
            seed_projects = [
                Project(
                    title=p["title"],
                    description=p["description"],
                    tech_stack=p["tech_stack"],
                    display_order=p["display_order"]
                ) for p in FALLBACK_PROJECTS
            ]
            db.session.add_all(seed_projects)
            db.session.commit()
            print("Database successfully seeded.")
    except Exception as e:
        print(f"Database initialization skipped or failed: {e}")


# --- API Routes ---

@app.route('/api/projects', methods=['GET'])
def api_projects():
    """Fetch all projects, ordered by display_order with fallback resilience"""
    try:
        projects = Project.query.order_by(Project.display_order.asc()).all()
        if projects and len(projects) > 0:
            return jsonify([proj.to_dict() for proj in projects]), 200
        return jsonify(FALLBACK_PROJECTS), 200
    except Exception as e:
        app.logger.error(f"Error fetching projects: {e}")
        return jsonify(FALLBACK_PROJECTS), 200

@app.route('/api/contact', methods=['POST'])
def api_contact():
    """Handle contact form submissions and save to DB."""
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON payload"}), 400
        
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()
    
    if not name or not email or not message:
        return jsonify({"status": "error", "message": "All fields are required."}), 400
    if not is_valid_email(email):
        return jsonify({"status": "error", "message": "Invalid email address format."}), 400
        
    try:
        new_msg = ContactMessage(name=name, email=email, message=message)
        db.session.add(new_msg)
        db.session.commit()
        return jsonify({"status": "success", "message": "Message delivered. I'll get back to you shortly."}), 201
    except Exception as e:
        app.logger.error(f"Error saving contact message: {e}")
        db.session.rollback()
        return jsonify({"status": "error", "message": "An internal server error occurred."}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200

# --- Static & Frontend Routes ---

@app.route('/')
def serve_index():
    """Serve main portfolio page"""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return send_from_directory(root_dir, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve photos, assets, or fallback to index.html"""
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    file_path = os.path.join(root_dir, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(root_dir, path)
    return send_from_directory(root_dir, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'True').lower() in ['true', '1', 't']
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
