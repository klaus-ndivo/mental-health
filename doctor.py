from flask import Blueprint, flash, get_flashed_messages, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from . import db
from .models import Appointment, Doctor, User, Survey
from datetime import datetime

doctor = Blueprint('doctor', __name__)

@doctor.route('/appointment/doctor/accept/<int:appointmentId>', methods=['POST'])
@login_required
def acceptAppointment(appointmentId):
    appointment = Appointment.query.get_or_404(appointmentId)
    
    appointmentDate = appointment.date
    numberOfAppointments = Appointment.query.filter_by(date=appointmentDate).count()
    if numberOfAppointments >= 5:
        flash('Sorry, there are no available sessions for this day', 'error')
    
    appointment.status = 'Accepted'
    db.session.commit()
    
    flash('Appointment accepted successfully', 'success')
    return redirect(url_for('main.professional'))

@doctor.route('/appointment/doctor/assign/<int:appointmentId>/<int:doctorId>', methods=['POST'])
@login_required
def assignDoctor(appointmentId, doctorId):
    appointment = Appointment.query.get_or_404(appointmentId)
    if appointment.status == 'Accepted':
        appointment.status = 'Assigned'
        appointment.doctorId = doctorId
        db.session.commit()
        flash('Doctor assigned successfully', 'success')
    
    return redirect(url_for('main.professional'))

@doctor.route('/doctor/chat-space', methods=['GET', 'POST'])
@login_required
def getSurveyComments():    
    return redirect(url_for('main.chatSpace'))

@doctor.route('/doctor/survey', methods=['GET', 'POST'])
@login_required
def getSurveyResults():
    # Query the database to get all surveys along with the user details
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
    
    # Query the database to get all surveys along with the user details
    surveys = db.session.query(Survey, User).join(User, Survey.userId == User.id).all()
    
    # Prepare data for the template
    survey_data = []
    for survey, user in surveys:
        for i, question in enumerate(questions, start=1):
            answer = getattr(survey, f'question{i}')
            survey_data.append({
                'fullname': user.fullname,
                'question': question,
                'answer': 'Yes' if answer else 'No'
            })
    
    
    return render_template('patientSurvey.html', survey_data=survey_data, active_page='survey', enumerate=enumerate)