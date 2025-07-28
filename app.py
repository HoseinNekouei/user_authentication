from flask import Flask, render_template,session, request, url_for, flash, session, redirect
import config
import secrets
# from flask_wtf import FlaskForm (I don't like use this module)

app = Flask(__name__)
app.config['SECRET_KEY'] =  config.SECRECT_KEY

def generate_crsf_token():
    if 'crsf_token' not in session:
        session['crsf_token']= secrets.token_hex(16)
    return session['crsf_token']

@app.route('/login', methods=['GET', 'POST'])
def login():
    riddle = "I am the ruler of systems, my name is short and clear. My secret is a mystery, a word that puzzles the ear."
    csrf_token= generate_crsf_token()

    # Get form data
    if request.method == 'POST':
        # Verify CSRF token
        if request.form.get('csrf_token') != session.get('csrf_token'):
            flash('Invalid CSRF token.', category='danger')
            return render_template('login.html', riddle= riddle, csrf_token= csrf_token)
        
        username = request.form.get('username')
        password= request.form.get('password')

        # validation user and password
        if not username:
            flash('Username is is required.', 'danger')
            return render_template('login.html', riddle= riddle, csrf_token= csrf_token)
        
        if not password:
            flash('Password is is required.', 'danger')
            return render_template('login.html', riddle= riddle, csrf_token= csrf_token)

        # check credintials
        if username == config.USERNAME and password== config.PASSWORD:
            flash('Login successful. You solved the pazzle!', 'success')
            return redirect(url_for('index.html'))
        else:
            flash('Invalid username or password. Try solving the riddle again.', 'danger')
    else:
        return redirect(url_for('login.html', riddle=riddle, csrf_token=csrf_token))
    

@app.route('/')
def index():
    return render_template('index.html')

if '__name__==__main__':
    app.run(debug=True)

