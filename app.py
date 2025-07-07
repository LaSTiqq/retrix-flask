from flask import Flask, render_template, redirect, url_for, request, make_response, Response, session, jsonify
from flask_static_digest import FlaskStaticDigest
from flask_wtf.csrf import CSRFProtect
from flask_talisman import Talisman
from flask_mail import Message, Mail
from flask_babel import Babel, lazy_gettext as _
from config import Config
from utils import restricted_list, year
from forms import ContactForm
import requests
import re
import os

flask_static_digest = FlaskStaticDigest()

app = Flask(__name__)
app.config.from_object(Config)

flask_static_digest.init_app(app)


def get_locale():
    lang = request.args.get('lang')
    if lang in ['lv', 'en', 'ru']:
        return lang
    if 'lang' in session:
        return session['lang']
    return request.accept_languages.best_match(['lv', 'en', 'ru']) or 'lv'


babel = Babel(app, locale_selector=get_locale)

csrf = CSRFProtect(app)
talisman = Talisman(app, content_security_policy=None, force_https=False)
mail = Mail(app)


@app.route("/", methods=["GET"])
def index():
    current_year = year()
    form = ContactForm()
    lang = get_locale()

    if "Googlebot" in request.user_agent.string:
        lang = request.accept_languages.best_match(['lv', 'ru', 'en']) or 'lv'

    response = make_response(render_template(
        'index.html', form=form, current_year=current_year, current_locale=lang
    ))
    response.headers['Content-Language'] = lang
    return response


@app.route("/send-ajax", methods=["POST"])
def send_ajax():
    form = ContactForm()
    if form.validate_on_submit():
        if any(restricted_list(form[field].data) for field in ['name', 'subject', 'message']):
            return jsonify({"status": "warning", "message": _("Jūs ievadījāt kaut ko neatļautu! Mēģiniet vēlreiz.")}), 400

        recaptcha_response = request.form.get('g-recaptcha-response')
        secret_key = os.getenv('RECAPTCHA_PRIVATE_KEY')
        verification_url = "https://www.google.com/recaptcha/api/siteverify"
        response = requests.post(verification_url, data={
            'secret': secret_key,
            'response': recaptcha_response
        })
        result = response.json()
        if not result.get('success') or result.get('score', 0) < app.config['RECAPTCHA_REQUIRED_SCORE']:
            return jsonify({"status": "warning", "message": _("Captcha pārbaude netika izieta. Mēģiniet vēlreiz.")}), 400

        html_content = render_template(
            "email.html", name=form.name.data, sender=form.email.data, content=form.message.data)
        text_content = re.sub(r"<[^>]+>", "", html_content)

        try:
            msg = Message(
                subject=form.subject.data,
                sender=app.config['MAIL_USERNAME'],
                recipients=['lavrencij@inbox.lv'],
                body=text_content
            )
            msg.html = html_content
            mail.send(msg)
            return jsonify({"status": "success", "message": _("Vēstule nosūtīta!")})
        except Exception:
            return jsonify({"status": "danger", "message": _("Kaut kas nogāja greizi! Mēģiniet vēlreiz.")}), 500


@app.route('/setlang')
def setlang():
    lang = request.args.get('lang', 'lv')
    if lang not in ['lv', 'en', 'ru']:
        lang = 'lv'
    session['lang'] = lang
    return redirect(request.referrer or url_for('index'))


@app.context_processor
def inject_locale():
    return {'get_locale': get_locale}


@app.route('/sitemap.xml')
def sitemap_xml():
    content = render_template('crawlers/sitemap.xml')
    return Response(content, mimetype='application/xml')


@app.route('/robots.txt')
def robots_txt():
    content = render_template('crawlers/robots.txt')
    return Response(content, mimetype='text/plain')


@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        "error.html",
        error_code=404,
        error_message="Page Not Found",
        error_comment=_("Jūs esat nokļuvis uz neeksistējošu lapu.")
    ), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template(
        "error.html",
        error_code=500,
        error_message="Internal Server Error",
        error_comment=_(
            "Radās kļūda un serveris nespēja izpildīt Jūsu pieprasījumu.")
    ), 500
