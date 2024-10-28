from . import db
from flask_login import UserMixin 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    fullname = db.Column(db.String(1000), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), default='user', nullable=False)
    
    appointment = db.relationship('Appointment', backref='user', lazy=True)
    appointmentsAssigned = db.relationship('Appointment', backref='doctor', lazy=True)
    survey = db.relationship('Survey', backref='user', lazy=True)
    
    def __repr__(self):
        return f"User('{self.email}', '{self.fullname}', '{self.gender}'), '{self.role}'"
    
class Doctor(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='doctor', nullable=False)
    
    def __repr__(self):
        return f"Doctor('{self.email}', '{self.fullname}', '{self.mobile}'), '{self.role}'"
    
    
    
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telephone = db.Column(db.String(100), nullable=False)
    appointmentHours = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Pending', nullable=False)
    date = db.Column(db.Date, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctorId = db.Column(db.Integer, nullable=False, default='00')
    
    def __repr__(self):
        return f"Appointment('{self.fullname}', '{self.email}', '{self.telephone}', '{self.appointmentHours}', '{self.status}', '{self.date}', '{self.userId}', '{self.doctorId}')"
    
    
    
class Survey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctorId = db.Column(db.Integer, nullable=False, default=0)
    
    question1 = db.Column(db.Boolean, nullable=False)
    question2 = db.Column(db.Boolean, nullable=False)
    question3 = db.Column(db.Boolean, nullable=False)
    question4 = db.Column(db.Boolean, nullable=False)
    question5 = db.Column(db.Boolean, nullable=False)
    question6 = db.Column(db.Boolean, nullable=False)
    question7 = db.Column(db.Boolean, nullable=False)
    question8 = db.Column(db.Boolean, nullable=False)
    question9 = db.Column(db.Boolean, nullable=False)
    question10 = db.Column(db.Boolean, nullable=False)
    question11 = db.Column(db.Boolean, nullable=False)
    question12 = db.Column(db.Boolean, nullable=False)
    question13 = db.Column(db.Boolean, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    
    def __repr__(self):
        return f"Survey('{self.userId}', '{self.doctorId}', '{self.question1}', '{self.question2}', '{self.question3}', '{self.question4}', '{self.question5}', '{self.question6}', '{self.question7}', '{self.question8}', '{self.question9}', '{self.question10}', '{self.question11}', '{self.question12}', '{self.question13}', '{self.comment}')"
