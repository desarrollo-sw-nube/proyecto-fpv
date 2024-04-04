from flask import jsonify, request, Blueprint





operations_blueprint = Blueprint('operations', __name__)

@operations_blueprint.route('/task', methods=['POST'])
def crear_task():
    
    json = request.get_json()

    required_fields = ['file_name', 'timestamp', 'status']

    if not all([field in json for field in required_fields]):
        raise ApiError('Invalid request', 400)