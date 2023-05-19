import uuid
from passlib.hash import pbkdf2_sha256
from dataclasses import asdict
from flask import (
    Blueprint,
    session,
    redirect,
    render_template,
    current_app,
    flash,
    url_for
)

from movie_library.src.models.user import User
from movie_library.src.models.forms import RegisterForm, LoginForm

user_route = Blueprint("user_route", __name__, 
                       static_folder='static',
                       template_folder='tenplates')

#Add a new user
@user_route.route("/register", methods=["GET","POST"])
def register():
    if session.get("email"):
        return redirect("pages.homepage")
    
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            user_Id=uuid.uuid4().hex,
            email = form.email.data,
            password = pbkdf2_sha256.hash(form.password.data)
        )

        current_app.db.user.insert_one(asdict(user))
        flash("User Registered Successfully!", "success")
        return redirect(url_for(".login"))


    return render_template("register.html", 
                           title="CinemaCatalog - Register User",
                           form = form)

# User Login
@user_route.route("/login", methods=["GET", "POST"])
def login():
    if session.get("email"):
        redirect(url_for("pages.homepage"))

    form = LoginForm()

    if form.validate_on_submit():
        user_db = current_app.db.user.find_one({"email": form.email.data}, {'_id': 0})

        if not user_db:
            flash("Login credentials are incorrect!", category="danger")
            return redirect(url_for(".login"))
        
        user = User(**user_db)
        
        if user and pbkdf2_sha256.verify(form.password.data, user.password):
            session["user_Id"] = user.user_Id
            session["email"] = user.email

            flash("Login Successful!", category="success")
            return redirect(url_for("pages.homepage"))
        
        flash("Login credentials are incorrect!", category="danger")

    return render_template("login.html", 
                           title="CinemaCatalog - User Login", 
                           form=form)

@user_route.route("/logout")
def logout():
    theme = session["theme"]
    session.clear()
    session["theme"] = theme

    return redirect(url_for(".login"))