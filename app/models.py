from . import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    has_whatsapp = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='participant') # admin, participant
    language = db.Column(db.String(5), default='es')
    location = db.Column(db.String(100), nullable=True) # For Shabbat detection
    points = db.Column(db.Integer, default=0)
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=True)

class Parasha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_es = db.Column(db.String(100))
    name_en = db.Column(db.String(100))
    name_he = db.Column(db.String(100))
    week_start = db.Column(db.Date)
    week_end = db.Column(db.Date)
    questions = db.relationship('Question', backref='parasha', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parasha_id = db.Column(db.Integer, db.ForeignKey('parasha.id'), nullable=False)
    text_es = db.Column(db.Text)
    text_en = db.Column(db.Text)
    text_he = db.Column(db.Text)
    option_a_es = db.Column(db.String(255))
    option_a_en = db.Column(db.String(255))
    option_a_he = db.Column(db.String(255))
    option_b_es = db.Column(db.String(255))
    option_b_en = db.Column(db.String(255))
    option_b_he = db.Column(db.String(255))
    option_c_es = db.Column(db.String(255))
    option_c_en = db.Column(db.String(255))
    option_c_he = db.Column(db.String(255))
    correct_option = db.Column(db.String(1)) # 'a', 'b', or 'c'

class Participation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    parasha_id = db.Column(db.Integer, db.ForeignKey('parasha.id'), nullable=False)
    score = db.Column(db.Integer)
    is_eligible = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donor_name = db.Column(db.String(100))
    amount = db.Column(db.Float)
    donation_type = db.Column(db.String(50)) # le'iluy nishmat, refua, hazlaja, otro
    recipient_name = db.Column(db.String(255)) # e.g., Rivka Live bat Rujel
    parasha_id = db.Column(db.Integer, db.ForeignKey('parasha.id'), nullable=True)
    duration_type = db.Column(db.String(20), default='single') # single, monthly, yearly
    weeks_count = db.Column(db.Integer, default=1)
    status = db.Column(db.String(20), default='confirmed') # confirmed, pending
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    parasha = db.relationship('Parasha', backref='donations', lazy=True)

class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    question = db.relationship('Question', backref='user_answers', lazy=True)

class HalajaAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('halaja_question.id'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    question = db.relationship('HalajaQuestion', backref='user_answers', lazy=True)

class HalajaCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_es = db.Column(db.String(100))
    name_en = db.Column(db.String(100))
    name_he = db.Column(db.String(100))
    icon = db.Column(db.String(20)) # Emoji or icon name
    questions = db.relationship('HalajaQuestion', backref='category', lazy=True)

class HalajaQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('halaja_category.id'), nullable=False)
    text_es = db.Column(db.Text)
    text_en = db.Column(db.Text)
    text_he = db.Column(db.Text)
    option_a_es = db.Column(db.String(255))
    option_a_en = db.Column(db.String(255))
    option_a_he = db.Column(db.String(255))
    option_b_es = db.Column(db.String(255))
    option_b_en = db.Column(db.String(255))
    option_b_he = db.Column(db.String(255))
    option_c_es = db.Column(db.String(255))
    option_c_en = db.Column(db.String(255))
    option_c_he = db.Column(db.String(255))
    correct_option = db.Column(db.String(1)) # 'a', 'b', or 'c'

class GlobalSetting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.String(255))
    description = db.Column(db.Text)

class RaffleResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    winner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    parashot_included = db.Column(db.String(255)) # List of names or IDs

    winner = db.relationship('User', backref='won_raffles')

class Advertisement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    line_1 = db.Column(db.String(100))
    line_2 = db.Column(db.String(100))
    line_3 = db.Column(db.String(100))
    line_4 = db.Column(db.String(100))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    link_url = db.Column(db.String(255))
    position = db.Column(db.String(10), default='right') # left, right
    amount_paid = db.Column(db.Float, default=0.0)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active') # active, expired
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
