from flask import Blueprint, session, redirect
from pyIvr import dynamiqueIvr
from pyIvr import render

ivrDemo = Blueprint('DynamiqueIvr', __name__)


@ivrDemo.route("/ivr/")
@ivrDemo.route("/ivr/<step>")
def ivr(step=None):
    if 'ivr' not in session:
        # Si aucun IVR charge alors on retourne au /
        return redirect('/')
    else:
        # Si un IVR est charge on essaye de l'afficher
        return make_response(step)


@render('vxml', '2.0')
def make_response(step=None):
    # Creation d'une reponse.
    json_loader = dynamiqueIvr(stringJson=session['ivr'])
    if step is None:
        step = json_loader.getParams()['begin']
    return json_loader.getParamAndStep(step, True, 'ivr/')


# Generation du SVI d'erreur
def get_error_svi():
    session['ivr'] = """{
  "params": {
    "begin": "errorMessage"
  },
  "svi":{
    "errorMessage": {
      "type": "message",
      "parametre": {
        "ressource": {
          "son": "/static/error.wav",
          "text": "Introuvable"
        },
        "idBlock": "errorMessage",
        "nextId": "end"
      }
    },
    "end": {
      "type": "disconnect",
      "parametre": {
        "idBlock": "end"
      }
    }
  }
}"""
