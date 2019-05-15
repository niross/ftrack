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
    starling_webhook_secret = StringField(
        _l('Starling Personal Webhook Production Secret'),
        validators=[
            DataRequired(),
            Length(min=36, max=36)
        ]
    )
    submit = SubmitField(label=_l('Connect'))
