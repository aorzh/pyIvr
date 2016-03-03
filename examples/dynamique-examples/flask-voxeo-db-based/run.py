from flask import Flask, session, request, redirect

# Import de la session pour les requete SQL.
from database import db_session

# Import des models
from models import Demo

# Import des blueprint
from blueprint_ivr import ivrDemo, get_error_svi
from blueprint_ivrIhm import ivrIhmDemo

# Declaration de l'application
app = Flask(__name__)
app.secret_key = 'li4Q~wNV7%RO?3=r.s|am^3>V:.cY22N%*>+%i=p/B6!1-HMv!/a8w@]Fk2n'

# Register des blueprints
app.register_blueprint(ivrDemo)
app.register_blueprint(ivrIhmDemo, url_prefix='/ihm')


@app.route("/")
def main():

    print session
    if 'calledid' not in session:
        get_error_svi()
    return redirect('/ivr/')


@app.route('/favicon.ico')
def empty():
    return ""


# Fonction appele a chaque appel HTTP
@app.before_request
def before_request():
    """
    If a session.calledid is happening in parameter then the backup
    in order to recover the SVI corresponding to the number called.

    In the case of the session.calledid Voxeo is happening in GET parameter
    the first call.
    """
    calledid = request.args.get('session.calledid', '')
    if calledid is not "":
        session['calledid'] = calledid
        try:
            session['ivr'] = Demo.query.filter(Demo.number == calledid).first().value
        except StandardError:
            get_error_svi()


# Permet de fermer la connexion mySQL.
@app.teardown_request
def shutdown_session(exception):
    db_session.remove()


if __name__ == '__main__':
    app.run(debug=False)
