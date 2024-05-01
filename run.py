# Flask modules
from flask import Flask, render_template, request, url_for, request, redirect, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_talisman import Talisman
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

# Other modules
from urllib.parse import urlparse, urljoin

import os
from dotenv import load_dotenv
load_dotenv()

# Local imports
from user import User, Anonymous

# from email_utility import send_email, send_registration_email, send_message_email
# from verification import confirm_token


# Create app
app = Flask(__name__)

# Configuration
# config = configparser.ConfigParser()
# config.read('configuration.ini')
# default = config['DEFAULT']
# app.secret_key = default['SECRET_KEY']
# app.config['MONGO_DBNAME'] = default['MONGO_DBNAME'] # os.environ.get('MONGO_DBNAME')
# app.config['MONGO_URI'] = default['MONGO_URI'].strip('\'"') #default['MONGO_URI']
# app.config['PREFERRED_URL_SCHEME'] = "https"

app.secret_key = os.environ.get('SECRET_KEY')
print(os.environ.get('SECRET_KEY'))
app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME') # os.environ.get('MONGO_DBNAME')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI').strip('\'"') #default['MONGO_URI']
app.config['PREFERRED_URL_SCHEME'] = "https"

# Create Pymongo
mongo = PyMongo(app)

# Create Bcrypt
bc = Bcrypt(app)

# Create Talisman
csp = {
    'default-src': [
        '\'self\'',
        'https://stackpath.bootstrapcdn.com',
        'https://pro.fontawesome.com',
        'https://code.jquery.com',
        'https://cdnjs.cloudflare.com'
    ]
}
talisman = Talisman(app, content_security_policy=csp)

# Create CSRF protect
csrf = CSRFProtect()
csrf.init_app(app)

# Create login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.anonymous_user = Anonymous
login_manager.login_view = "login"


# ROUTES

# Index
@app.route('/')
def index():
    return render_template('index.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            # Redirect to index if already authenticated
            return redirect(url_for('index'))
        # Render login page
        return render_template('login.html', error=request.args.get("error"))
    # Retrieve user from database
    users = mongo.db.users
    user_data = users.find_one({'email': request.form['email']}, {'_id': 0})
    if user_data:
        # Check password hash
        if bc.check_password_hash(user_data['password'], request.form['pass']):
            # Create user object to login (note password hash not stored in session)
            user = User.make_from_dict(user_data)
            login_user(user)

            # Check for next argument (direct user to protected page they wanted)
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)

            # Go to profile page after login
            return redirect(next or url_for('index'))

    # Redirect to login page on error
    return redirect(url_for('login', error=1))


# Register
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Trim input data
        email = request.form['email'].strip()
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()
        password = request.form['pass'].strip()

        users = mongo.db.users
        # Check if email address already exists
        existing_user = users.find_one(
            {'email': email}, {'_id': 0})

        if existing_user is None:
            logout_user()
            # Hash password
            hashpass = bc.generate_password_hash(password).decode('utf-8')
            # Create user object (note password hash not stored in session)
            new_user = User(first_name, last_name, email)
            # Create dictionary data to save to database
            user_data_to_save = new_user.dict()
            user_data_to_save['password'] = hashpass

            # Insert user record to database
            if users.insert_one(user_data_to_save):
                login_user(new_user)
                # send_registration_email(new_user)
                return redirect(url_for('index'))
            else:
                # Handle database error
                return redirect(url_for('register', error=2))

        # Handle duplicate email
        return redirect(url_for('register', error=1))

    # Return template for registration page if GET request
    return render_template('register.html', error=request.args.get("error"))


# Logout
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile', methods=['GET'])
@login_required
def profile():
    # Retrieve user's config from MongoDB
    user_data = mongo.db.users.find_one({'id': current_user.id}, {'config': 1})
    user_config = user_data.get('config', {}) if user_data else {}

    # Pass user's config and notes to the profile template
    return render_template('profile.html', current_config=user_config)


# Save config
@app.route('/save_config', methods=['POST'])
@login_required
def save_config():
    # Extract other configuration values
    minimum_savings_threshold = int(request.form.get("minimum_savings_threshold"))
    cleanup_days_threshold = int(request.form.get("cleanup_days_threshold"))
    maximum_posts_per_session = int(request.form.get("maximum_posts_per_session"))
    delay_between_posts = int(request.form.get("delay_between_posts"))
    delay_between_sessions = int(request.form.get("delay_between_sessions"))
    recently_updated_hour_threshold = int(request.form.get("recently_updated_hour_threshold"))
    special_message_threshold = int(request.form.get("special_message_threshold"))
    random_image_toggle = request.form.get("random_image_toggle")
    associate_tag = request.form.get("associate_tag")
    start_time = request.form.get("start_time")
    end_time = request.form.get("end_time")
    fb_group_link = request.form.get("fb_group_link")
    fb_page_id = request.form.get("fb_page_id")
    access_token = request.form.get("access_token")
    
    # Extract login data
    logins = []
    emails = request.form.getlist("email[]")
    passwords = request.form.getlist("password[]")
    for email, password in zip(emails, passwords):
        logins.append({"email": email, "password": password})

    # Update user's config with new values
    current_user.update_config({
        "minimum_savings_threshold": minimum_savings_threshold,
        "cleanup_days_threshold": cleanup_days_threshold,
        "maximum_posts_per_session": maximum_posts_per_session,
        "delay_between_posts": delay_between_posts,
        "delay_between_sessions": delay_between_sessions,
        "recently_updated_hour_threshold": recently_updated_hour_threshold,
        "special_message_threshold": special_message_threshold,
        "random_image_toggle": random_image_toggle,
        "associate_tag": associate_tag,
        "start_time": start_time,
        "end_time": end_time,
        "fb_group_link": fb_group_link,
        "fb_page_id": fb_page_id,
        "access_token": access_token,
        "logins": logins  # Add logins to config
    })

    # Update the user's config in the database
    users = mongo.db.users
    users.update_one({"id": current_user.id}, {"$set": {"config": current_user.get_config()}})
    return "Success! Config updated"


# Route to start the config
@app.route('/start_config', methods=['POST'])
@login_required
def start_config():
    # Update the user's config in the database to set 'running' to True
    users = mongo.db.users
    users.update_one({"id": current_user.id}, {"$set": {"running": True}})
    return "Config started"


# Route to stop the config
@app.route('/stop_config', methods=['POST'])
@login_required
def stop_config():
    # Update the user's config in the database to set 'running' to False
    users = mongo.db.users
    users.update_one({"id": current_user.id}, {"$set": {"running": False}})
    return "Config stopped"



# Messages
# @app.route('/messages', methods=['GET'])
# @login_required
# def messages():
#     all_users = mongo.db.users.find(
#         {"id": {"$ne": current_user.id}}, {'_id': 0})
#     inbox_messages = mongo.db.messages.find(
#         {"to_id": current_user.id, "deleted": False}).sort("timestamp", -1)
#     sent_messages = mongo.db.messages.find(
#         {"from_id": current_user.id, "deleted": False, "hidden_for_sender": False}).sort("timestamp", -1)
#     return render_template('messages.html', users=all_users, inbox_messages=inbox_messages, sent_messages=sent_messages)



# Confirm email
# @app.route('/confirm/<token>', methods=['GET'])
# def confirm_email(token):
#     logout_user()
#     try:
#         email = confirm_token(token)
#         if email:
#             if mongo.db.users.update_one({"email": email}, {"$set": {"verified": True}}):
#                 return render_template('confirm.html', success=True)
#     except:
#         return render_template('confirm.html', success=False)
#     else:
#         return render_template('confirm.html', success=False)


# Verification email
# @app.route('/verify', methods=['POST'])
# @login_required
# def send_verification_email():
#     if current_user.verified == False:
#         send_registration_email(current_user)
#         return "Verification email sent"
#     else:
#         return "Your email address is already verified"

# Send message
# @app.route('/send_message', methods=['POST'])
# @login_required
# def send_message():
#     title = request.form.get("title")
#     body = request.form.get("body")
#     from_id = current_user.id
#     from_name = current_user.display_name()
#     to_id = request.form.get("user")
#     to_user_dict = mongo.db.users.find_one({"id": to_id})
#     to_user = User.make_from_dict(to_user_dict)
#     to_name = to_user.display_name()


# Delete message
# @app.route('/delete_message', methods=['POST'])
# @login_required
# def delete_message():
#     message_id = request.form.get("message_id")
#     if mongo.db.messages.update_one({"id": message_id}, {"$set": {"deleted": True}}):
#         return "Success! Message deleted"
#     else:
#         return "Error! Could not delete message"


# Hide sent message
# @app.route('/hide_sent_message', methods=['POST'])
# @login_required
# def hide_sent_message():
#     message_id = request.form.get("message_id")
#     if mongo.db.messages.update_one({"id": message_id}, {"$set": {"hidden_for_sender": True}}):
#         return "Success! Message hidden from sender"
#     else:
#         return "Error! Could not hide message"


# Change Name
@app.route('/change_name', methods=['POST'])
@login_required
def change_name():
    first_name = request.form['first_name'].strip()
    last_name = request.form['last_name'].strip()

    if mongo.db.users.update_one({"email": current_user.email}, {"$set": {"first_name": first_name, "last_name": last_name}}):
        return "User name updated successfully"
    else:
        return "Error! Could not update user name"


# Delete Account
@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user_id = current_user.id

    # Deletion flags
    user_deleted = False
    notes_deleted = False
    messages_deleted = False

    # Delete user details
    if mongo.db.users.delete_one({"id": user_id}):
        user_deleted = True
        logout_user()

    # Delete notes
    if mongo.db.notes.delete_many({"user_id": user_id}):
        notes_deleted = True

    # Delete messages
    if mongo.db.messages.delete_many({"$or": [{"from_id": user_id}, {"to_id": user_id}]}):
        messages_deleted = True

    return {"user_deleted": user_deleted, "notes_deleted": notes_deleted, "messages_deleted": messages_deleted}


# LOGIN MANAGER REQUIREMENTS

# Load user from user ID
@login_manager.user_loader
def load_user(userid):
    # Return user object or none
    users = mongo.db.users
    user = users.find_one({'id': userid}, {'_id': 0})
    if user:
        return User.make_from_dict(user)
    return None


# Safe URL
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc

if __name__ == '__main__':
    app.run(debug=True)

# Heroku environment
# if os.environ.get('APP_LOCATION') == 'vercel':
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port)
# else:
#     app.run(host='localhost', port=8080, debug=True)
