from flask import Flask, render_template, redirect, request, session, flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
app.secret_key = 'ThisIsSecret!'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    session['first_name'] = request.form['first_name']
    session['last_name'] = request.form['last_name']
    session['email'] = request.form['email']
    session['password'] = request.form['password']
    session['confirm_password'] = request.form['confirm_password']

    name_valid = False
    email_valid = False
    password_valid = False
    password_match = False

    # First and Last Name cannot contain any numbers
    if len(session['first_name']) > 0 and len(session['last_name']) > 0 and session['first_name'].isalpha() and session['last_name'].isalpha():
        name_valid = True
    else:
        flash(u"Name must only be letters", "error")

    # Password should be more than 8 characters
    if len(session['password']) > 8:
        password_valid = True
    else:
        flash(u"Passworld should be more than 8 characters", "error")
        
    # Password and Confirm_password should match
    if session['password'] == session['confirm_password']:
        password_match = True
    else:
        flash(u"Passwords do not match", "error")

    # Email should be a valid email
    if EMAIL_REGEX.match(session['email']):
        email_valid = True
    else:
        flash(u"Invalid email address", "error")

    # If all submitted corrected properly, flash "Thanks for submitting your information"
    if name_valid and email_valid and password_valid and password_match:
        session.clear()
        flash(u"Thanks for submitting your information", "success")

    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)