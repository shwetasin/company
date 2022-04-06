from cmath import log
from datetime import datetime
from unicodedata import category

from flask import Flask, render_template, redirect, request, url_for
from flask_login import login_required, current_user, login_user, logout_user
from sqlalchemy import func

from company import Employee,Department,Manager,User,admin, db, login

global_all_department_no = None
global_all_department_name = None

app = Flask(__name__)
app.secret_key ='ItshoudlbeLongEnough'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] =False

db.init_app(app)
login.init_app(app)

login.login_view = 'login'

def get_all_department():
    global global_all_category_no, global_all_category_name
    all_department_info = db.session.query(Department.department_id,Department.department_name)
    all_department_info = list(all_department_info)
    global_all_department_no, global_all_department_name = zip(*all_department_info)

@app.before_first_request
def create_all():
    db.create_all()
    get_all_department()

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/blogs')
    if request.method == 'POST':
        email = request.form.get('email')
        user = user.query.filter_by(email=email).first()
        if user is not None and user.check_password(request.form.get('password')):
            login_user(user)
            return redirect('/blogs')
        return render_template('/register.html')
    return render_template('/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/register')
@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
       return redirect('/blogs')
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        if user.query.filter_by(email=email).first():
            return "Email Already Exists"

        user = user(email=email,username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect('/blogs')
    return render_template('register.html')


@app.route('/admin')
def admin():
    if current_user.is_authenticated:
        return render_template('/admin_home.html')
    return redirect(url_for('list_all_admin'))






@app.before_first_request
def create_all():
    db.create_all()
    get_all_department()


    if __name__ == '__main__':
         app.run(debug=True)