import ldap
from flask import request, render_template, flash, redirect, \
    url_for, Blueprint, g
from flask_login import current_user, login_user, logout_user, login_required
from ldapflask import login_manager, db
from ldapflask.auth.models import User, LoginForm
 
auth = Blueprint('auth', __name__)
 
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
 
@auth.before_request
def get_current_user():
    g.user = current_user
 
@auth.route('/')
@auth.route('/home')
def home():
    return render_template('home.html')
 
 
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        flash('You are already logged in.')
        return redirect(url_for('auth.home'))
 
    form = LoginForm(request.form)
 
    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')
 
        ## Check LDAP credentials here...
        try:
            User.try_login(username, password)
        except ldap.INVALID_CREDENTIALS:
            flash(
                'Invalid username or password. Please try again.',
                'danger')
            return render_template('login.html', form=form)
        except ldap.SERVER_DOWN:
            flash(
                'Cannot open TCP socket to the LDAP server.',
                'danger')
            return render_template('login.html', form=form)
 
        user = User.query.filter_by(username=username).first()
        # User doesn't exist in the db, create him
        if not user:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()

        # Use Flask-Login to formally login the user...
        login_user(user)

        flash('You have successfully logged in.', 'success')
        return redirect(url_for('auth.home'))
 
    if form.errors:
        flash(form.errors, 'danger')
 
    return render_template('login.html', form=form)
 
 
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.home'))
