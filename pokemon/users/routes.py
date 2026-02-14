from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user
from pokemon.models import User
from pokemon.extension import db, bcrypt

user_bp = Blueprint('users', __name__, template_folder='templates')

@user_bp.route('/')
def index():
  return render_template('users/index.html', title='Users Page')

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
  if request.method == 'POST':
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    query = db.select(User).where(User.username == username, User.email == email)
    user = db.session.scalar(query)
    if user:
      flash('Username or Email already exists!', 'warning')
    else:
      if password == confirm_password:
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash('Register successfully!', 'success')
        return redirect(url_for('users.login'))
      else:
        flash('Password not Matched!', 'warning')
        
  return render_template('users/register.html', title='Register Page')

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    query = db.select(User).where(User.username == username)
    user = db.session.scalar(query)
    if user:
      if bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return redirect(url_for('users.index'))
      else:
        flash('Password is not matched!', 'warning')
    else:
      flash('Username is not exists!', 'warning')

  return render_template('users/login.html', title='Login Page')

@user_bp.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('core.index'))

@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
  user = db.session.get(User, current_user.id)
  if request.method == 'POST':
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    
    user.firstname = firstname
    user.lastname = lastname

    db.session.commit()
    flash('Update profile successfully!', 'success')
    return redirect(url_for('users.index'))
  
  return render_template('users/profile.html', title='Profile Page', user=user)