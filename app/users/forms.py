from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class StarlingAuthForm(FlaskForm):
    starling_auth_code = StringField(
        _l('Starling Personal Access Token'),
        validators=[
            DataRequired(),
            Length(min=64, max=64)
        ]
    )
    submit = SubmitField(label=_l('Connect'))
