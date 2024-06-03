from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm): # Create form class
    username = StringField('Username', # Label for field
                           validators=[DataRequired(),                      # Validating presence
                                        Length(min=2, max=20)],             # and length.
                                        render_kw = {"placeholder": "anon"})
    password = PasswordField('Password', # Label for password field
                            validators=[DataRequired(),            # Validating presence
                                        Length(min=8, max=64),      # and length again.
                                        EqualTo('confirm', message='Passwords must match')], # Make sure its equal to the confirm field as well
                                        render_kw = {"placeholder": "password"})
    confirm = PasswordField('Confirm Password',
                            validators=[DataRequired()],
                            render_kw = {"placeholder": "password"})
    tnc = BooleanField('I accept the Terms and Conditions', validators=[DataRequired()]) # Just make sure people have something to show they're all good.
    submit = SubmitField('Sign Up') # Submit button

class LoginForm(FlaskForm): # Create yet another form class
    username = StringField('Username', # Label for field
                           validators=[DataRequired()], # Validating presence (we're only checking data this time so there's not much need for a length check)
                           render_kw = {"placeholder": "anon"}) 
    password = PasswordField('Password', # Label for password field
                            validators=[DataRequired()], # Validating presence
                            render_kw = {"placeholder": "password"})
    remember = BooleanField('Remember Me') # Remember me checkbox
    submit = SubmitField('Login') # Submit
