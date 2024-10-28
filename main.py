from datetime import datetime
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import Appointment, Survey, User
from . import db
# from .models import OrderItem, Product, Order, OrderDetails

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/home')
def home():
    return render_template('home.html', active_page='home')

@main.route('/survey')
@login_required
def survey():
    questions = [
            "I relapse way too easily in my drinking/smoking habit",
            "I feel sad and unhappy",
            "I have interest and joy in the aspects of my life that were of major importance to me",
            "I feel like I fall in everything I try",
            "I have difficulty in concentration and making of decisions",
            "I got constant anxiety and panic attacks",
            "I am agitated and keep moving around",
            "I am constantly looking over my shoulder in fear",
            "I feel like the urge to move on from my negative thought is lacking",
            "I live too much in my head, creating negative ideas, thoughts that will only bring me harm",
            "I feel fatigued",
            "I feel trapped or caught",
            "Most of the times I am broke I get mad"
        ]
    return render_template('survey.html', active_page='survey', questions=questions, enumerate=enumerate)

@main.route('/professional')
@login_required
def professional():
    return render_template('professional.html', active_page='professional')

@main.route('/About')
def About():
    return render_template('About.html', active_page='About')

@main.route('/journal')
def journal():
    return render_template('journal.html', active_page='journal')

@main.route('/chat')
def chat():
    return render_template('chat.html', active_page='chat')

@main.route('/appointment/book')
def appointment():
    return render_template('appointment.html', active_page='Appointment')

@main.route('/appointment/doctor')
def doctorAppointment():
    appointments =  Appointment.query.all()
    return render_template('doctorAppointment.html', active_page='doctorAppointment', appointments=appointments)

@main.route('/userpanel')
def userPanel():
    appointments = Appointment.query.filter_by(userId=current_user.id).all()
    return render_template('userpanel.html', active_page='userpanel', appointments=appointments)

@main.route('/doctor/chat-space')
def chatSpace():
    comments = db.session.query(Survey.comment, User.fullname).join(User, Survey.userId == User.id).all()
    return render_template('chatSpace.html', active_page='chatSpace', comments=comments)