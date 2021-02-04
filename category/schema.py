from flask_restx import fields,reqparse
from rest import api

from utils import parser_utils


CategorySchema = api.model('Category', {
    'id': fields.String(required=False, description='Category id.'),
    'name': fields.String(required=True, description='Category name min 3, max 50.'),
})

CategoryParser = reqparse.RequestParser()
CategoryParser.add_argument('name', type=parser_utils.validate_string(50, 3), required=True, location='json')
