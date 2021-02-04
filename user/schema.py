from flask_restx import fields,reqparse
from rest import api

from utils import parser_utils


LoginRegisterSchema = api.model('User', {
    'username': fields.String(required=True, description='User username min 5, max 50.'),
    'password': fields.String(required=True, description='User password min 5, max 50.'),
})

LoginRegisterParser = reqparse.RequestParser()
LoginRegisterParser.add_argument('username', type=parser_utils.validate_string(50, 5), required=True, location='json')
LoginRegisterParser.add_argument('password', type=parser_utils.validate_string(50, 5), required=True, location='json')
