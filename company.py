from unicodedata import category
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from enum import unique

db = SQLAlchemy()
login = LoginManager()

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(250))

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)
    
class Department(db.Model):
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String, nullable = False)
    employee = db.relationship('Employee', backref='department',lazy=True)

class Employee(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    employee_id = db.Column(db.Integer,db.ForeignKey('department.department_id'), nullable=False)
    email = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    password = db.Column(db.Text, nullable=False)
    in_creation_date = db.Column(db.DateTime)
    out_creation_date = db.Column(db.DateTime)

class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Manager_id = db.Column(db.Integer,db.ForeignKey('Employee.id'), nullable=True)
    password = db.Column(db.Text, nullable=False)
    manager_in_time = db.Column(db.DateTime)
    manager_out_time = db.Column(db.DateTime)

class admin(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.department_id'), nullable=False)
    email = db.Column(db.Integer,db.ForeignKey('users.id'), nullable=False)
    password = db.Column(db.Text, nullable=False)
    designation= db.Column(db.text)
    phone_number = db.Column(db.text)
    permanent_address=db.Column(db.text)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    