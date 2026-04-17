import os
from flask import Flask, render_template, request, abort, url_for, session, redirect
import os # Make sure os is imported for getenv to work

app = Flask(__name__)
app.secret_key = 'any_random_string_here' # Required to encrypt the session cookie

app.config['username'] = os.getenv('username')
app.config['password'] = os.getenv('password')

# Configuration
DATA_FILE = 'book_entries.json'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def hello():
    # Check if the user is actually logged in
    if not session.get('logged_in'):
        return redirect(url_for('index')) # Send them back to login page
        
    return render_template('home.html')

@app.route('/login')
def index():

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def result():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == app.config['username'] and password == app.config['password']:
        # 1. Store the login status in the session
        session['logged_in'] = True
        session['user'] = username
        
        # 2. Redirect to the 'hello' function (the / route)
        return redirect(url_for('hello')) 
    else:
        return abort(401)

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

@app.route('/api/entries', methods=['GET'])
def get_entries():
    """Get all book entries"""
    entries = load_entries()
    # Sort by date (newest first)
    entries.sort(key=lambda x: x['date'], reverse=True)
    return jsonify(entries)

@app.route('/api/entries', methods=['POST'])
def add_entry():
    """Add new book entry"""
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
    save_entries([])
    return jsonify({'message': 'All entries cleared'})

@app.route('/upload', methods=['POST'])
def upload_image():
    """Upload book cover image"""
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
    entries = load_entries()
    return jsonify(entries)

if __name__ == '__main__':
    # Create data file if it doesn't exist
    if not os.path.exists(DATA_FILE):
        save_entries([])

if __name__ == '__main__':
    app.run(debug = True, port=9000)