from flask_restx import Api

authorizations = {
    'apiKey': {
            'type': 'apiKey',
            'description': 'Personal API Key authorization',
            'name': 'Authorization',
            'in': 'header',
    }
}
api = Api(version='1.0', title='Ad API', description='Ad API', authorizations=authorizations, security='apiKey')
