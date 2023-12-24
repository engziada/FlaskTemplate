from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, SelectField
from wtforms.validators import  DataRequired, EqualTo, Length, Email


# Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


# Add User Form
class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    rank = SelectField('Role', choices=[(1, 'Admin'), (2, 'Employee'), (3, 'Customer')], coerce=int)
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=8),  # Enforce minimum length
        EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Add User')


# Edit User Form
class EditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    rank = SelectField('Role', choices=[(1, 'Admin'), (2, 'Employee'), (3, 'Customer')], coerce=int)
    submit = SubmitField('Save Changes')
