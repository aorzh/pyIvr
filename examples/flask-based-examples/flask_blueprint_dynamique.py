from flask import Flask
from pyIvr.ext.flask.blueprintFlaskIvr import ivrBlueprint

app = Flask(__name__)
app.register_blueprint(ivrBlueprint)

app.run(debug=True)
