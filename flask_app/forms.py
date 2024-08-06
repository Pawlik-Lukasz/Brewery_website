from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, Email, Length, EqualTo, Regexp, ValidationError
from flask_app.models import User


class Registration(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('password_confirm',
                                                                              message="Passwords have to be identical"),
                                                     Length(min=6, max=60),
                                                     Regexp(
                                                         regex=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&+=]).*$",
                                                         message="Password should contain at least one letter, one number and one special sign")])
    password_confirm = PasswordField("Confirm password", validators=[InputRequired(),
                                                                     Length(min=6, max=60)])
    email = StringField("Email", validators=[InputRequired(), Email(message="Type correct email address")])
    submit = SubmitField('Sign Up!')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(message="User with this name already exists. Change Your username")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(message="User with this email already exists. Change Your email")


class Login(FlaskForm):
    email = StringField('Email',
                        validators=[InputRequired(), Email()])

    password = PasswordField("Password",
                             validators=[InputRequired(), Length(min=6, max=60)])

    submit = SubmitField('Sign In!')
