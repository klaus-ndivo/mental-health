from flask import Blueprint, flash, get_flashed_messages, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from . import db
from .models import Appointment, Doctor, User, Survey
from datetime import datetime

client = Blueprint('client', __name__)

@client.route('/appointment/book', methods=['POST'])
@login_required
def bookAppointment():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        telephone = request.form.get('telephone')
        appointmentHours = request.form.get('appointmentHours')
        date = request.form.get('date')
        
        dateNew = datetime.strptime(date, '%d/%m/%Y').date()
        
        newAppointment = Appointment(fullname=fullname, email=email, telephone=telephone, appointmentHours=appointmentHours, date=dateNew, userId=current_user.id)
        
        db.session.add(newAppointment)
        db.session.commit()
        
        flash('Appointment booked successfully', 'success')
        return redirect(url_for('main.userPanel'))
    
    return redirect(url_for('main.Appointments'))

@client.route('/appointment/modify/<int:appointmentId>', methods=['POST'])
@login_required
def modifyAppointment(appointmentId):
    appointment = Appointment.query.get_or_404(appointmentId)
    if appointment.userId != current_user.id:
        flash('You are not authorized to modify this appointment', 'error')
        return redirect(url_for('main.userPanel'))
    
    appointment.fullname = request.form.get('fullname')
    appointment.email = request.form.get('email')
    appointment.telephone = request.form.get('telephone')
    appointment.appointmentHours = request.form.get('appointmentHours')
    appointment.date = datetime.strptime(request.form.get('date'), '%d/%m/%Y').date()
    db.session.commit()
    
    flash('Appointment modified successfully', 'success')
    
    return redirect(url_for('main.userPanel'))

@client.route('/appointment/delete/<int:appointmentId>', methods=['POST'])
@login_required
def deleteAppointment(appointmentId):
    appointment = Appointment.query.get_or_404(appointmentId)
    if appointment.userId != current_user.id:
        flash('You are not authorized to delete this appointment', 'error')
        return redirect(url_for('main.userPanel'))
    
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment deleted successfully', 'success')
    return redirect(url_for('main.userPanel'))

@client.route('/survey/submit', methods=['POST'])
@login_required
def submitSurvey():
    if request.method == 'POST':
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
        
        # Check that all questions are answered
        for i in range(len(questions)):
            if request.form.get('question' + str(i + 1)) is None:
                flash('Please answer all questions', 'error')
                return redirect(url_for('main.survey'))

        # Helper function to convert string values to boolean
        def to_bool(value):
            return value.lower() == 'true'

        # Capture and convert answers to boolean
        answers = [to_bool(request.form.get('question' + str(i + 1))) for i in range(len(questions))]
        
        comment = request.form.get('comment')

        # Create a new Survey instance
        newSurvey = Survey(
            userId=current_user.id,
            question1=answers[0],
            question2=answers[1],
            question3=answers[2],
            question4=answers[3],
            question5=answers[4],
            question6=answers[5],
            question7=answers[6],
            question8=answers[7],
            question9=answers[8],
            question10=answers[9],
            question11=answers[10],
            question12=answers[11],
            question13=answers[12],
            comment=comment
        )

        # Add the new survey to the session and commit
        db.session.add(newSurvey)
        db.session.commit()

        flash('Survey submitted successfully', 'success')
        return redirect(url_for('main.userPanel'))

    return redirect(url_for('main.survey'))

