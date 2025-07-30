from flask import (
    Flask,
    render_template,
    session, request, 
    url_for, 
    flash, session, 
    redirect)

import config
import secrets
import re
# from flask_wtf import FlaskForm (I don't like use this module)

app = Flask(__name__)
app.config['SECRET_KEY'] =  config.SECRECT_KEY

def generate_crsf_token():
    if 'csrf_token' not in session:
        session['csrf_token']= secrets.token_hex(16)
    return session['csrf_token']

@app.route('/', methods=['GET', 'POST'])
def login():
    riddle = "I am the ruler of systems, my name is short and clear. My secret is a mystery, a word that puzzles the ear."

    # Get form data
    if request.method == 'POST':
        # Verify CSRF token
        if request.form.get('csrf_token') != session.get('csrf_token'):
            flash('Invalid CSRF token.', category='danger')
            return render_template('login.html', csrf_token= generate_crsf_token(), riddle=riddle)
        
        username = request.form.get('username')
        password= request.form.get('password')
        username = re.sub(r'[^a-z]', '', username)  # Remove any leading 'a-z' characters
        password = re.sub(r'[^a-z]', '', password)   # Remove any leading 'a-z' characters

        # validation user and password
        if not username:
            flash('Username is is required.', 'danger')
            return render_template('login.html', csrf_token= generate_crsf_token())
        
        if not password:
            flash('Password is is required.', 'danger')
            return render_template('login.html', csrf_token= generate_crsf_token())

        # check credintials
        if username == config.USERNAME and password== config.PASSWORD:
            session.pop('csrf_token', None)  # Clear token after successful login
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Try solving the riddle again.', 'danger')
            return render_template('login.html', csrf_token= generate_crsf_token(), riddle=riddle)
    else:
        return render_template('login.html', csrf_token=generate_crsf_token(), riddle=riddle)
    

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if '__name__==__main__':
    app.run(debug=True)