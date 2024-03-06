from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MAIL_SERVER'] = 'smtp.yourmailprovider.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_email_password'

mail = Mail(app)

users = {}  # In a real application, use a database to store user information

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['signupEmail']
    password = request.form['signupPassword']

    if email in users:
        flash('Email already registered. Please log in.')
        return redirect(url_for('home'))

    confirmation_code = secrets.token_urlsafe(16)
    users[email] = {'password': password, 'confirmed': False, 'confirmation_code': confirmation_code}

    # Send confirmation email
    msg = Message('Confirm Your Email', sender='your_email@example.com', recipients=[email])
    msg.body = f"Your confirmation code is: {confirmation_code}\n\nVisit {request.url_root}confirm/{email}/{confirmation_code} to confirm your email."
    mail.send(msg)

    flash('Sign
