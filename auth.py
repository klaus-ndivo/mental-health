from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user, login_user, logout_user
from . import db
from .models import User, Doctor

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    
    if not email or not password:
        flash('Please fill all details', 'error')
        return redirect(url_for('auth.login'))
        
    user = User.query.filter_by(email=email).first()
    
    if not user or not check_password_hash(user.password, password):
        user = Doctor.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Please check your details and try again', 'error')
            return redirect(url_for('auth.login'))
        
        session['role'] = 'doctor'
        session['user_id'] = user.id
        login_user(user, remember=remember)
        
        return redirect(url_for('main.professional'))    
        
    session['role'] ='user'
    session['user_id'] = user.id
    login_user(user, remember=remember)
    
    return redirect(url_for('main.userPanel'))    

@auth.route('/signup')
def signUp():
    return render_template('signUp.html')

@auth.route('/signup', methods=['POST'])
def signUp_post():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    gender = request.form.get('gender')
    
    user= User.query.filter_by(email=email).first()
    if user:
        flash('Email address already exists', 'error')
        return redirect(url_for('auth.signUp'))
    
    new_user = User(fullname=fullname, email=email, gender=gender, password=generate_password_hash(password, method='pbkdf2:sha256'), role='user')
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('auth.login'))

@auth.route('/professional-signup')
def professionalSignUp():
    return render_template('professionalSignUp.html')

@auth.route('/professional-signup', methods=['POST'])
def professionalSignUp_post():
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    mobile = request.form.get('mobile')
    
    user= Doctor.query.filter_by(email=email).first()
    
    if user:
        flash('Email address already exists', 'error')
        return redirect(url_for('auth.professionalSignUp'))
    
    new_user = Doctor(fullname=fullname, email=email, mobile=mobile, password=generate_password_hash(password, method='pbkdf2:sha256'), role='doctor')
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('main.index'))