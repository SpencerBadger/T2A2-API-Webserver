from init import app
from marshmallow.exceptions import ValidationError
from blueprints.shows_bp import shows_bp
from blueprints.cli_bp import db_commands
from blueprints.users_bp import users_bp

app.register_blueprint(db_commands)
app.register_blueprint(shows_bp)
app.register_blueprint(users_bp)

@app.route("/")
def index():
    return "Operational"

@app.errorhandler(ValidationError)
def invalid_request(err):
    return {'error': vars(err)['messages']}, 400

@app.errorhandler(KeyError)
def missing_key(err):
    return {'error': (f"Missing field: {str(err)}")}, 400

@app.errorhandler(405)
@app.errorhandler(404)
def not_found(err):
    return {'error': 'not found'}, 404