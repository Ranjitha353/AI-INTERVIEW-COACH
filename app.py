from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
from flask import render_template, request, redirect, flash
from flask_login import login_user
from werkzeug.security import check_password_hash

app.config['SECRET_KEY'] = 'your_secret_key'



# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# =========================
# USER MODEL
# =========================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    full_name = db.Column(db.String(150))
    industry = db.Column(db.String(150))
    bio = db.Column(db.Text)
    current_role = db.Column(db.String(150))
    experience = db.Column(db.String(50))
    target_job = db.Column(db.String(150))
    target_company = db.Column(db.String(150))
    skills = db.Column(db.Text)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# =========================
# HOME
# =========================
from flask import render_template

@app.route('/')
def home():
    return render_template('home.html')



# =========================
# REGISTER
# =========================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered!"

        # hash password (VERY IMPORTANT)
        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        # automatically login after register
        login_user(new_user)

        return redirect(url_for('dashboard'))

    return render_template('register.html')




# =========================
# LOGIN
# =========================
from flask import render_template, request, redirect, flash
from flask_login import login_user
from werkzeug.security import check_password_hash

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect("/dashboard")
        else:
            flash("Invalid username or password")

    return render_template("login.html")





# =========================
# DASHBOARD
# =========================
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)




# =========================
# PROFILE
# =========================
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    if request.method == "POST":
        current_user.full_name = request.form["full_name"]
        current_user.industry = request.form["industry"]
        current_user.bio = request.form["bio"]
        current_user.current_role = request.form["current_role"]
        current_user.experience = request.form["experience"]
        current_user.target_job = request.form["target_job"]
        current_user.target_company = request.form["target_company"]
        current_user.skills = request.form["skills"]

        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("profile.html", user=current_user)



# =========================
# LOGOUT
# =========================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)





