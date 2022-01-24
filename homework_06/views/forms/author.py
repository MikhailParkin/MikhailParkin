from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email


class AuthorForm(FlaskForm):
    name = StringField("Author name", validators=[DataRequired()])
    email = StringField("Author e-mail", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
