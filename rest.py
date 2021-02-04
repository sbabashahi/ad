from flask_restx import Api

from utils.exceptions import CustomException

authorizations = {
    'apiKey': {
            'type': 'apiKey',
            'description': 'Personal API Key authorization',
            'name': 'Authorization',
            'in': 'header',
    }
}
api = Api(version='1.0', title='Ad API', description='Ad API', authorizations=authorizations, security='apiKey')


@api.errorhandler(CustomException)
def custom_error(error):
    return {'message': error.detail}, error.status_code
