from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify, current_app, session
from werkzeug.utils import secure_filename
import os
from utils.topic_modeling import run_topic_modeling, analyze_statistics, analyze_sentiments
from create_app import create_app, db
from models import AnalyzedFile, RecentActivity
import json
import numpy as np
from datetime import datetime

app = create_app()

def convert_to_serializable(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj

def format_topics(topics):
    formatted_topics = []
    for topic in topics:
        topic_id, terms = topic
        formatted_terms = [term.split('*')[1].strip('" ') for term in terms.split(' + ')]
        interpreted_topic = interpret_topic(formatted_terms)
        formatted_topics.append({"id": topic_id, "terms": formatted_terms, "interpretation": interpreted_topic})
    return formatted_topics

def interpret_topic(terms):
    """
    A simple function to generate a human-readable interpretation of a topic.
    You can customize this function based on your specific needs and domain knowledge.
    """
    if "gift" in terms and "card" in terms:
        return "Gift Cards"
    elif "amazon" in terms:
        return "Amazon Services"
    elif "easy" in terms and "quick" in terms:
        return "Ease of Use"
    elif "great" in terms and "love" in terms:
        return "Positive Feedback"
    else:
        return "General"

def get_analyzed_files():
    files = AnalyzedFile.query.all()
    analyzed_files = []
    for file in files:
        topics = json.loads(file.topics) if file.topics else []
        formatted_topics = format_topics(topics)
        analyzed_files.append({
            "filename": file.filename,
            "topics": formatted_topics
        })
    return analyzed_files

def save_analyzed_file(filename, topics, visualizations, statistics, sentiments):
    topics = json.dumps(topics, default=convert_to_serializable)
    visualizations = json.dumps(visualizations, default=convert_to_serializable)
    statistics = json.dumps(statistics, default=convert_to_serializable)
    sentiments = json.dumps(sentiments, default=convert_to_serializable)

    existing_file = AnalyzedFile.query.filter_by(filename=filename).first()
    if existing_file:
        existing_file.topics = topics
        existing_file.visualizations = visualizations
        existing_file.statistics = statistics
        existing_file.sentiments = sentiments
        existing_file.timestamp = datetime.utcnow()
    else:
        new_file = AnalyzedFile(
            filename=filename,
            topics=topics,
            visualizations=visualizations,
            statistics=statistics,
            sentiments=sentiments,
            timestamp=datetime.utcnow()
        )
        db.session.add(new_file)
    
    recent_activity = RecentActivity(action="Uploaded/Analyzed", filename=filename, timestamp=datetime.utcnow())
    db.session.add(recent_activity)
    
    db.session.commit()

def delete_analyzed_file(filename):
    file = AnalyzedFile.query.filter_by(filename=filename).first()
    if file:
        db.session.delete(file)
        db.session.commit()
        
        recent_activity = RecentActivity(action="Deleted", filename=filename, timestamp=datetime.utcnow())
        db.session.add(recent_activity)
        db.session.commit()

def calculate_average_sentiment(files):
    return 0.5

def calculate_total_topics(files):
    return len(files) * 5

def get_recent_activities():
    activities = RecentActivity.query.order_by(RecentActivity.timestamp.desc()).limit(10).all()
    return [{"action": activity.action, "filename": activity.filename, "timestamp": activity.timestamp} for activity in activities]

def get_sentiment_counts():
    return {"positive": 10, "neutral": 5, "negative": 2}

def get_topic_data():
    return {"labels": ["Topic 1", "Topic 2", "Topic 3"], "counts": [10, 15, 5]}

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    analyzed_files = get_analyzed_files()
    total_files = len(analyzed_files)
    average_sentiment_score = calculate_average_sentiment(analyzed_files)
    total_topics = calculate_total_topics(analyzed_files)
    recent_activities = get_recent_activities()
    sentiment_counts = get_sentiment_counts()
    topic_data = get_topic_data()

    return render_template('dashboard.html', 
                           analyzed_files=analyzed_files, 
                           total_files=total_files, 
                           average_sentiment_score=average_sentiment_score, 
                           total_topics=total_topics,
                           recent_activities=recent_activities,
                           positive_count=sentiment_counts['positive'],
                           neutral_count=sentiment_counts['neutral'],
                           negative_count=sentiment_counts['negative'],
                           topic_labels=topic_data['labels'],
                           topic_counts=topic_data['counts'])

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        topics, visualizations = run_topic_modeling(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        statistics = analyze_statistics(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        sentiments = analyze_sentiments(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        save_analyzed_file(filename, topics, visualizations, statistics, sentiments)
        return jsonify({'success': True})

@app.route('/results/<filename>')
def results(filename):
    file_record = AnalyzedFile.query.filter_by(filename=filename).first()
    if not file_record:
        return "File not found", 404

    topics = json.loads(file_record.topics)
    visualizations = json.loads(file_record.visualizations)
    statistics = json.loads(file_record.statistics)
    sentiments = json.loads(file_record.sentiments)
    
    return render_template('results.html', filename=filename, topics=topics, visualizations=visualizations, statistics=statistics, sentiments=sentiments)

@app.route('/topics/<filename>')
def topics(filename):
    file_record = AnalyzedFile.query.filter_by(filename=filename).first()
    if not file_record:
        return "File not found", 404

    topics = json.loads(file_record.topics)
    visualizations = json.loads(file_record.visualizations)
    return render_template('topics.html', filename=filename, topics=topics, visualizations=visualizations)

@app.route('/statistics/<filename>')
def statistics(filename):
    file_record = AnalyzedFile.query.filter_by(filename=filename).first()
    if not file_record:
        return "File not found", 404
    
    statistics = json.loads(file_record.statistics)
    return render_template('statistics.html', filename=filename, statistics=statistics)

@app.route('/sentiments/<filename>')
def sentiments(filename):
    file_record = AnalyzedFile.query.filter_by(filename=filename).first()
    if not file_record:
        return "File not found", 404
    
    sentiments = json.loads(file_record.sentiments)
    return render_template('sentiments.html', filename=filename, sentiments=sentiments)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        session['num_topics'] = int(request.form['num_topics'])
        session['num_passes'] = int(request.form['num_passes'])
        session['num_words'] = int(request.form['num_words'])
        return redirect(url_for('settings'))
    
    settings = {
        'num_topics': session.get('num_topics', 5),
        'num_passes': session.get('num_passes', 10),
        'num_words': session.get('num_words', 4)
    }
    return render_template('settings.html', settings=settings)

@app.route('/notifications')
def notifications():
    notifications = [
        {"title": "New Feature", "content": "We have added new sentiment analysis feature."},
        {"title": "Maintenance", "content": "Scheduled maintenance on May 25th, 2024."}
    ]
    return render_template('notifications.html', notifications=notifications)

@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        delete_analyzed_file(filename)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'File not found'}), 404

@app.route('/clear_recent_activity', methods=['POST'])
def clear_recent_activity():
    try:
        num_deleted = db.session.query(RecentActivity).delete()
        db.session.commit()
        return jsonify({'success': True, 'deleted': num_deleted})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return redirect(url_for('dashboard'))

    results = AnalyzedFile.query.filter(AnalyzedFile.filename.contains(query)).all()
    analyzed_files = []
    for file in results:
        topics = json.loads(file.topics) if file.topics else []
        formatted_topics = format_topics(topics)
        analyzed_files.append({
            "filename": file.filename,
            "topics": formatted_topics
        })

    total_files = len(analyzed_files)
    average_sentiment_score = calculate_average_sentiment(analyzed_files)
    total_topics = calculate_total_topics(analyzed_files)
    recent_activities = get_recent_activities()
    sentiment_counts = get_sentiment_counts()
    topic_data = get_topic_data()

    return render_template('dashboard.html',
                           analyzed_files=analyzed_files,
                           total_files=total_files,
                           average_sentiment_score=average_sentiment_score,
                           total_topics=total_topics,
                           recent_activities=recent_activities,
                           positive_count=sentiment_counts['positive'],
                           neutral_count=sentiment_counts['neutral'],
                           negative_count=sentiment_counts['negative'],
                           topic_labels=topic_data['labels'],
                           topic_counts=topic_data['counts'])

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], 'favicon.ico')

if __name__ == '__main__':
    app.run(debug=True)
