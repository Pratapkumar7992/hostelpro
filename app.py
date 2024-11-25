from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json
import os
import secrets

app = Flask(__name__)

# Define paths for JSON files
ISSUE_DATA_FILE = 'issues/issues_reportissues.json'
ADMIN_CREDENTIALS_FILE = 'issues/admin_credentials.json'
RESOLVE_DATA_FILE = 'issues/resolve.json'
STUDENT_CREDENTIALS_FILE = 'issues/student_credentials.json'

# Secret key for session management
app.secret_key = secrets.token_hex(16)  # Generates a 32-character random string

# Ensure the directory exists
os.makedirs(os.path.dirname(ISSUE_DATA_FILE), exist_ok=True)
os.makedirs(os.path.dirname(ADMIN_CREDENTIALS_FILE), exist_ok=True)
os.makedirs(os.path.dirname(RESOLVE_DATA_FILE), exist_ok=True)
os.makedirs(os.path.dirname(STUDENT_CREDENTIALS_FILE), exist_ok=True)

# Helper functions to load and save issues, admin credentials, and student credentials
def load_issues():
    try:
        if os.path.exists(ISSUE_DATA_FILE):
            with open(ISSUE_DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading issues: {e}")
        return []

def save_issues(data):
    try:
        with open(ISSUE_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print("Issues saved successfully.")
    except IOError as e:
        print(f"Error saving issues: {e}")

def load_admin_credentials():
    try:
        if os.path.exists(ADMIN_CREDENTIALS_FILE):
            with open(ADMIN_CREDENTIALS_FILE, 'r') as f:
                return json.load(f)
        else:
            return {"email": "admin@example.com", "password": "password123"}  # Default credentials for testing
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading admin credentials: {e}")
        return {}

def save_admin_credentials(credentials):
    try:
        with open(ADMIN_CREDENTIALS_FILE, 'w') as f:
            json.dump(credentials, f, indent=4)
        print("Admin credentials saved successfully.")
    except IOError as e:
        print(f"Error saving admin credentials: {e}")

def load_student_credentials():
    try:
        if os.path.exists(STUDENT_CREDENTIALS_FILE):
            with open(STUDENT_CREDENTIALS_FILE, 'r') as f:
                return json.load(f)  # Returns a list of dictionaries
        else:
            return []  # Empty list if file doesn't exist
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading student credentials: {e}")
        return []

def save_student_credentials(credentials):
    try:
        with open(STUDENT_CREDENTIALS_FILE, 'w') as f:
            json.dump(credentials, f, indent=4)
        print("Student credentials saved successfully.")
    except IOError as e:
        print(f"Error saving student credentials: {e}")

def load_resolved_issues():
    try:
        if os.path.exists(RESOLVE_DATA_FILE):
            with open(RESOLVE_DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            return []
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading resolved issues: {e}")
        return []

def save_resolved_issues(data):
    try:
        with open(RESOLVE_DATA_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print("Resolved issues saved successfully.")
    except IOError as e:
        print(f"Error saving resolved issues: {e}")

@app.route('/')
def index():
    return render_template('index.html')  # Make sure you have an index.html template


@app.route('/')
def report_issue():
    return render_template('index.html')

@app.route('/lock-issues')
def lock_issues():
    return render_template('report_issue.html')

@app.route('/water-issue')
def water_issue():
    return render_template('report_issue.html')

@app.route('/light-issue')
def light_issue():
    return render_template('report_issue.html')

@app.route('/food-quality-issue')
def food_quality_issue():
    return render_template('report_issue.html')

@app.route('/study-room-issue')
def study_room_issue():
    return render_template('report_issue.html')

@app.route('/submit-issue', methods=['POST'])
def submit_issue():
    issue_data = {
        "issue_type": "general",  # You can change this based on issue type
        "name": request.form['name'],
        "email": request.form['email'],
        "room_number": request.form['room-number'],
        "issue_description": request.form['issue-description']
    }
    issues = load_issues()
    issues.append(issue_data)
    save_issues(issues)
    return jsonify({'message': 'Issue reported successfully!'})

# Student Login Route
@app.route('/student-login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        issue_type = request.form['issue_type']  # Get the selected issue type

        credentials_list = load_student_credentials()  # This returns a list of dictionaries

        # Check if the email exists in the list and if the password matches
        student = next((cred for cred in credentials_list if cred['email'] == email), None)

        if student is None:
            flash("Incorrect email.")
            return redirect(url_for('student_login'))

        if student['password'] != password:
            flash("Incorrect password.")
            return redirect(url_for('student_login'))
        
        # Redirect to a page based on the selected issue type (example: dynamic redirection)
        if issue_type == 'water_issue':
            return redirect(url_for('water_issue'))
        elif issue_type == 'light_issue':
            return redirect(url_for('light_issue'))
        elif issue_type == 'food_quality_issue':
            return redirect(url_for('food_quality_issue'))
        elif issue_type == 'study_room_issue':
            return redirect(url_for('study_room_issue'))
        elif issue_type=='lock_issue':
            return redirect(url_for('lock_issues'))
        
        # If no issue type selected, redirect to a default page
        return redirect(url_for('facility'))

    return render_template('student_login.html')


# Student Register Route
@app.route('/student-register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Load existing student credentials
        credentials_list = load_student_credentials()

        # Check if the email already exists
        if any(cred['email'] == email for cred in credentials_list):
            flash("Email already registered!")
            return redirect(url_for('student_register'))

        # Add the new student credentials to the list
        credentials_list.append({'email': email, 'password': password})

        # Save the updated credentials back to the JSON file
        save_student_credentials(credentials_list)

        flash("Registration successful! Please log in.")
        return redirect(url_for('student_login'))  # Redirect to login page after successful registration

    return render_template('student_register.html')

@app.route('/facility')
def facility():
    resolved_issues = load_resolved_issues()
    return render_template('facility.html', resolved_issues=resolved_issues)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        credentials = load_admin_credentials()

        if email != credentials['email']:
            flash("Incorrect email.")
            return redirect(url_for('admin_login'))
        if password != credentials['password']:
            flash("Incorrect password.")
            return redirect(url_for('admin_login'))
        
        return redirect(url_for('admin_dashboard'))

    return render_template('admin_login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    issues = load_issues()
    return render_template('admin_dashboard.html', issues=issues)

@app.route('/resolve-issue/<int:issue_id>', methods=['POST'])
def resolve_issue(issue_id):
    issues = load_issues()
    resolved_issues = load_resolved_issues()

    print("Current issues:", issues)  # Debug print
    print("Resolved issues:", resolved_issues)  # Debug print

    if issue_id < len(issues):
        resolved_issue = issues.pop(issue_id)
        resolved_issues.append(resolved_issue)

        save_issues(issues)
        save_resolved_issues(resolved_issues)

        flash("Issue resolved successfully!")
        return redirect(url_for('admin_dashboard'))

    return jsonify({'error': 'Issue not found'}), 404

@app.route('/resolve')
def resolve_issues():
    resolved_issues = load_resolved_issues()
    print("Fetched resolved issues:", resolved_issues)  # Debug print
    return render_template('resolve.html', resolved_issues=resolved_issues)







@app.route('/')
def hello():
    return jsonify({"message": "Hello, from HealthSphere!"})

# Vercel uses this entry point for serverless functions
def handler(req, res):
    return app(req, res)



if __name__ == '__main__':
    app.run(debug=True)