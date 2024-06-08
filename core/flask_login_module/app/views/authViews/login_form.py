from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Which actor is your favorite?', validators=[DataRequired(), Length(10, 40)])
    password = PasswordField('Password')
    submit = SubmitField('Submit')