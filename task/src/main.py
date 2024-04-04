from flask import Flask, jsonify
import os 


app = Flask(__name__)

app.register_blueprint(operations_blueprints)


app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "msg": err.description,
        "version": os.environ.get("VERSION")
    }
    return jsonify(response), err.code