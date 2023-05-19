from flask_wtf import FlaskForm
from wtforms import (
    StringField, 
    IntegerField, 
    SubmitField, 
    TextAreaField, 
    URLField,
    PasswordField
)
from wtforms.validators import (
    InputRequired, 
    NumberRange, 
    EqualTo, 
    Length,
    Email
)

class MovieForm(FlaskForm):
    name = StringField("Movie Name", validators=[InputRequired()])
    director = StringField("Director", validators=[InputRequired()])
    year = IntegerField("Release Year", 
                        validators=[InputRequired(), 
                                    NumberRange(min=1850, message="Year not supported")]
                        )
    submit = SubmitField("Add Movie")

class StringListField(TextAreaField):
    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            self.data = [ line.strip() for line in valuelist[0].split("\n")]
        else:
            self.data = []

    def _value(self):
        if self.data:
            return "\n".join(self.data)
        else:
            return ""
        
class ExtendedMovieForm(MovieForm):
    writers = StringListField("Writers")
    plot = StringField("Plot")
    cast = StringListField("Cast")
    genre = StringListField("Genres")
    video_link = URLField("Video Link")

    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", 
                            validators=[InputRequired(),
                                        Length(min=8, message="Password should be atleast 8 characters long.")])
    confirm_password = PasswordField("Confirm Password", 
                                    validators=[InputRequired(), 
                                                EqualTo("password", message="Passwords does not match.")])
    
    submit = SubmitField("Add User")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", 
                            validators=[InputRequired()])
    
    submit = SubmitField("Login")