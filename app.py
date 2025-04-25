import os
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read the CSV file
        df = pd.read_csv(filepath)
        
        # Get basic information
        preview = df.head().to_html()
        summary = df.describe().to_html()
        columns = df.columns.tolist()
        
        return jsonify({
            'preview': preview,
            'summary': summary,
            'columns': columns
        })
    
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/visualize', methods=['POST'])
def visualize():
    data = request.json
    column = data.get('column')
    chart_type = data.get('chart_type')
    
    if not column or not chart_type:
        return jsonify({'error': 'Missing parameters'}), 400
    
    # Read the most recent CSV file
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if not files:
        return jsonify({'error': 'No data file found'}), 400
    
    latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(app.config['UPLOAD_FOLDER'], x)))
    df = pd.read_csv(os.path.join(app.config['UPLOAD_FOLDER'], latest_file))
    
    # Create the visualization
    plt.figure(figsize=(10, 6))
    
    if chart_type == 'bar':
        df[column].value_counts().plot(kind='bar')
    elif chart_type == 'line':
        df[column].plot(kind='line')
    elif chart_type == 'histogram':
        df[column].plot(kind='hist')
    
    plt.title(f'{chart_type.capitalize()} Chart of {column}')
    plt.xlabel(column)
    plt.ylabel('Count')
    
    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    # Convert to base64 for sending to frontend
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    
    return jsonify({'image': img_str})

if __name__ == '__main__':
    app.run(debug=True) 