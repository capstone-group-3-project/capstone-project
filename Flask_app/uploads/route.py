from flask import render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from utils.topic_modeling import run_topic_modeling
from create_app import create_app

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('results', filename=filename))

@app.route('/results/<filename>')
def results(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    topics, visualizations = run_topic_modeling(file_path)
    return render_template('results.html', topics=topics, visualizations=visualizations)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')
