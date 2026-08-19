from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy with no settings
db = SQLAlchemy()

class Project(db.Model):
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech_stack = db.Column(db.JSON, nullable=False)
    repo_url = db.Column(db.String(255), default='#')
    demo_url = db.Column(db.String(255), default='#')
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title, description, tech_stack, display_order=0, repo_url='#', demo_url='#'):
        self.title = title
        self.description = description
        self.tech_stack = tech_stack
        self.display_order = display_order
        self.repo_url = repo_url
        self.demo_url = demo_url

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "tech_stack": self.tech_stack,
            "repo_url": self.repo_url,
            "demo_url": self.demo_url,
            "display_order": self.display_order
        }

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message
