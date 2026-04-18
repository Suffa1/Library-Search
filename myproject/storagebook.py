from __main__ import app  # Borrow the app from app.py like signup.py does
from flask import render_template, request, jsonify, session, redirect, url_for
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename

# Configuration
DATA_FILE = 'book_entries.json'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create data file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

def load_entries():
    """Load entries from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_entries(entries):
    """Save entries to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(entries, f, indent=2)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/booklog')
def booklog():
    """Render the book log page - protected behind login"""
    if not session.get('logged_in'):
        return redirect(url_for('index'))
    return render_template('storagebook.html')

@app.route('/api/entries', methods=['GET'])
def get_entries():
    """Get all book entries"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    entries = load_entries()
    entries.sort(key=lambda x: x['date'], reverse=True)
    return jsonify(entries)

@app.route('/api/entries', methods=['POST'])
def add_entry():
    """Add new book entry"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()

    if not data or not data.get('book') or not data.get('date'):
        return jsonify({'error': 'Book title and date are required'}), 400

    entries = load_entries()

    new_entry = {
        'id': len(entries) + 1,
        'book': data['book'],
        'date': data['date'],
        'timestamp': datetime.now().isoformat(),
        'image': data.get('image', '')
    }

    entries.append(new_entry)
    save_entries(entries)

    return jsonify(new_entry), 201

@app.route('/api/entries/<int:entry_id>', methods=['DELETE'])
def delete_entry(entry_id):
    """Delete a specific entry"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    entries = load_entries()
    entries = [entry for entry in entries if entry['id'] != entry_id]

    # Reassign IDs
    for i, entry in enumerate(entries, 1):
        entry['id'] = i

    save_entries(entries)
    return jsonify({'message': 'Entry deleted'})

@app.route('/api/entries/clear', methods=['DELETE'])
def clear_all_entries():
    """Clear all entries"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    save_entries([])
    return jsonify({'message': 'All entries cleared'})

@app.route('/upload', methods=['POST'])
def upload_image():
    """Upload book cover image"""
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        return jsonify({
            'image': f"/static/uploads/{unique_filename}",
            'message': 'Image uploaded successfully'
        })

    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/export')
def export_entries():
    """Export entries as JSON"""
    if not session.get('logged_in'):
        return redirect(url_for('index'))

    entries = load_entries()
    return jsonify(entries)