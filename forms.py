from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Length
from flask_babel import lazy_gettext as _


class ContactForm(FlaskForm):
    name = StringField(
        label=_('Vārds'),
        id='name',
        render_kw={
            'class': 'form-control bg-transparent',
            'placeholder': _('Vārds'),
            'autocomplete': 'off',
            'value': _('Jānis'),
        },
        validators=[
            DataRequired(),
            Length(min=3, max=15)
        ],
    )
    email = EmailField(
        label=_('E-pasts'),
        id='email',
        render_kw={
            'class': 'form-control bg-transparent',
            'placeholder': _('E-pasts'),
            'autocomplete': 'off',
            'value': _('janis.celotajs@gmail.com'),
        },
        validators=[
            DataRequired(),
            Email()
        ],
    )
    subject = StringField(
        label=_('Temats'),
        id='subject',
        render_kw={
            'class': 'form-control bg-transparent',
            'placeholder': _('Temats'),
            'autocomplete': 'off',
            'value': _('Apgaismojums virtuvē'),
        },
        validators=[
            DataRequired(),
            Length(min=5, max=30)
        ],
    )
    message = TextAreaField(
        label=_('Ziņojums'),
        id='message',
        render_kw={
            'class': 'form-control bg-transparent',
            'placeholder': _('Ziņojums'),
            'autocomplete': 'off',
        },
        validators=[
            DataRequired(),
            Length(min=20)
        ],
    )
