from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, Length
from flask_babel import lazy_gettext as _


class ContactForm(FlaskForm):
    name = StringField(
        label=_('Vārds'),
        render_kw={
            'class': 'form-control bg-transparent mb-2',
            'placeholder': _('Jānis'),
            'autocomplete': 'off',
        },
        validators=[
            DataRequired(),
            Length(min=3, max=15)
        ],
    )
    email = EmailField(
        label=_('E-pasts'),
        render_kw={
            'class': 'form-control bg-transparent mb-2',
            'placeholder': _('janis.celotajs@gmail.com'),
            'autocomplete': 'off',
        },
        validators=[
            DataRequired(),
            Email()
        ],
    )
    subject = StringField(
        label=_('Temats'),
        render_kw={
            'class': 'form-control bg-transparent mb-2',
            'placeholder': _('LED gaismas virtuvē'),
            'autocomplete': 'off',
        },
        validators=[
            DataRequired(),
            Length(min=5, max=30)
        ],
    )
    message = TextAreaField(
        label=_('Teksts'),
        render_kw={
            'class': 'form-control bg-transparent pt-3',
            'placeholder': _('Vēlos izgaismot virtuvi, ko Jūs varat piedāvāt?'),
            'autocomplete': 'off',
            'rows': 6,
        },
        validators=[
            DataRequired(),
            Length(min=50)
        ],
    )
