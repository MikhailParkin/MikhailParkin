from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email
from wtforms_sqlalchemy.fields import QuerySelectField

from models import Author


class AuthorForm(FlaskForm):
    name = StringField("Author name", validators=[DataRequired()])
    email = StringField("Author e-mail", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    body = StringField("Body", validators=[DataRequired()])
    user_id = QuerySelectField(query_factory=lambda: Author.query.all(), get_label='name')
