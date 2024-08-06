from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from flask_app import app, db, bcrypt
from flask_app.forms import Registration, Login
from flask_app.models import User, Brewery
import requests
import random


@app.route("/")
def home():
    return render_template(template_name_or_list="index.html",
                           title="Home")


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        brewery_search = request.form["message"]
        breweries = requests.get(url=f"https://api.openbrewerydb.org/v1/breweries/search?query={brewery_search}")
        breweries_json = breweries.json()
        try:
            random_breweries = random.sample(breweries_json, 5)
            return render_template(template_name_or_list="results.html",
                                   breweries=random_breweries,
                                   title="Results")
        except ValueError:
            flash("Sorry, there are no breweries that match Your search query", category="error")
            return render_template(template_name_or_list="index.html")
    else:
        return render_template(template_name_or_list="search.html",
                               title="Search")


@app.route("/favourites", methods=["GET", "POST"])
@login_required
def favourites():
    if request.method == "GET":
        with open('flask_app/fav_brew.txt', 'r', encoding='utf-8') as f:
            list_of_brews = []
            [list_of_brews.append(eval(line)) for line in f.readlines()]

        return render_template(template_name_or_list="favourites.html",
                               list_of_brews=list_of_brews,
                               title="Favourites")
    else:
        with open('flask_app/fav_brew.txt', 'a', encoding='utf-8') as f:
            f.write(request.form["chosen-brewery"] + '\n')
        flash("Your brewery was added to Your favourites", category="success")
        return redirect(url_for('home'))


@app.route('/deleted', methods=["POST"])
def delete_fav():
    with open("flask_app/fav_brew.txt", "r") as f:
        lines = f.readlines()
    with open('flask_app/fav_brew.txt', 'w', encoding='utf-8') as f:
        for line in lines:
            if request.form["brewery-delete"] not in line:
                f.write(line)
    flash(f'Your favourite brewery {request.form["brewery-delete"]} was deleted :(', category="success")
    return redirect(url_for('home'))


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Registration()
    if form.validate_on_submit():
        encrypted_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=encrypted_pass)
        db.session.add(user)
        db.session.commit()
        flash("Signed Up properly, You can now log in", category="success")
        return redirect(url_for('home'))
    return render_template(template_name_or_list="register.html",
                           form=form,
                           title="Sign Up")


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Login()
    if form.validate_on_submit and request.method == "POST":
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("You are now logged in", category="success")
            return redirect(url_for('home'))
        else:
            flash("Login unsuccessful. Please check email and password", category="error")
            return redirect(url_for('home'))
    return render_template(template_name_or_list="login.html",
                           form=form,
                           title="Sign Up")


@app.route('/logout')
def logout():
    logout_user()
    flash("You have successfully logged out", category="success")
    return redirect(url_for('home'))


@app.route('/account')
@login_required
def account():
    return render_template(template_name_or_list="account.html",
                           title="Account")
