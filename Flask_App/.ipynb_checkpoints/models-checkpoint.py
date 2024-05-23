from create_app import db
from datetime import datetime

class AnalyzedFile(db.Model):
    __tablename__ = 'analyzed_files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, unique=True, nullable=False)
    topics = db.Column(db.Text, default='[]')  # Store topics as a JSON string
    visualizations = db.Column(db.Text, default='[]')  # Store visualizations as a JSON string
    statistics = db.Column(db.Text, default='{}')  # Store statistics as a JSON string
    sentiments = db.Column(db.Text, default='{}')  # Store sentiments as a JSON string
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Store the timestamp of the activity

class RecentActivity(db.Model):
    __tablename__ = 'recent_activities'
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String, nullable=False)
    filename = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
