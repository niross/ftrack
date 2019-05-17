from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import PasswordInput


class PlatformAuthForm(FlaskForm):
    starling_auth_code = StringField(
        _l('Starling Personal Access Token'),
        widget=PasswordInput(hide_value=False),
        validators=[
            DataRequired(),
            Length(min=64, max=64)
        ]
    )
    starling_webhook_secret = StringField(
        _l('Starling Personal Webhook Secret'),
        widget=PasswordInput(hide_value=False),
        validators=[
            DataRequired(),
            Length(min=36, max=36)
        ]
    )
    ynab_auth_code = StringField(
        _l('YNAB Personal Access Token'),
        widget=PasswordInput(hide_value=False),
        validators=[
            DataRequired(),
            Length(min=64, max=64)
        ]
    )
    ynab_account_id = SelectField(
        _l('Select your Starling Account on YNAB'),
        choices=[(None, '-- Select an Account --')]
    )
    ynab_category_id = SelectField(
        _l('Select your Default Category'),
        choices=[(None, '-- Select a Category --')]
    )
    submit = SubmitField(label=_l('Save'))
