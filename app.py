from flask import Flask, render_template, request
from controller.ControlAuth import *
from controller.ControlGrade import *
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import Config
from controller import db


# Initialize Flask
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Silakan login untuk mengakses halaman ini.'
login_manager.login_message_category = 'info'

# User loader function for flask-login
@login_manager.user_loader
def load_user(user_id):
    from model.ModulUser import User
    return User.query.get(int(user_id))

# =============== AUTH ROUTES ===============

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        return login_post()
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        return signup_post()
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout_route():
    return logout()

# =============== MAIN ROUTES ===============

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    ipk, total_sks = calculate_ipk()
    semester_summary = get_semester_summary()
    grade_dist = get_grade_distribution()
    return render_template('dashboard.html', ipk=ipk, total_sks=total_sks, semester_summary=semester_summary, grade_dist=grade_dist)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/creator')
def creator():
    return render_template('ghifar.html')

# =============== GRADE ROUTES ===============

@app.route('/grades')
@login_required
def halaman_grade():
    grades = get_all_grades()
    ipk, total_sks = calculate_ipk()
    semester_summary = get_semester_summary()
    return render_template('grades.html', grades=grades, ipk=ipk, total_sks=total_sks, semester_summary=semester_summary)

@app.route('/add-grade', methods=['GET', 'POST'])
@login_required
def tambah_nilai():
    if request.method == 'POST':
        return add_grade()
    return render_template('add_grade.html')

@app.route('/delete-grade/<int:grade_id>')
@login_required
def hapus_nilai(grade_id):
    return delete_grade(grade_id)

@app.route('/edit-grade/<int:grade_id>', methods=['GET', 'POST'])
@login_required
def edit_nilai(grade_id):
    if request.method == 'POST':
        return edit_grade(grade_id)
    
    grade = get_grade_by_id(grade_id)
    if not grade or grade.user_id != current_user.id:
        flash("Data nilai tidak ditemukan!", "error")
        return redirect(url_for('halaman_grade'))
    
    return render_template('edit_grade.html', grade=grade)

# Create tables on first run
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
