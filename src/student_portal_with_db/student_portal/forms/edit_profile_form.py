from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length
from flask_wtf.file import FileField, FileAllowed

class EditProfileForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(min=2, max=80)]
    )

    age = IntegerField(
        "Age",
        validators=[DataRequired(), NumberRange(min=1, max=120)]
    )

    profile_pic = FileField(
        "Profile Picture",
        validators=[FileAllowed(["jpg", "png", "jpeg"], "Images only!")]
    )

    submit = SubmitField("Save Changes")
