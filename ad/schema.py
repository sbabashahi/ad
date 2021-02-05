from flask_restx import fields,reqparse
from rest import api

from utils import parser_utils


MediaSchema = api.model('Media', {
    'id': fields.String(required=False, description='Media id.'),
    'path': fields.String(required=True, description='Media path 10, max 200.'),
})

MediaParser = reqparse.RequestParser()
MediaParser.add_argument('id', type=parser_utils.validate_int(min_length=1), required=False, location='json')
MediaParser.add_argument('path', type=parser_utils.validate_string(200, 10), required=True, location='json')


UserSchema = api.model('User', {
    'username': fields.String(required=True, description='User username.'),
})


CategorySchema = api.model('Category', {
    'id': fields.Integer(required=True, description='Category id.'),
    'name': fields.String(required=False, description='Category name.'),
})


AdSchema = api.model('Ad', {
    'id': fields.String(readonly=True),
    'title': fields.String(required=True, description='Title of Ad'),
    'body': fields.String(required=True, description='Body of Ad'),
    'user': fields.Nested(UserSchema, required=True, description='Ad Creator'),
    'created': fields.Integer(readonly=True, description='Ad create  epoch time'),
    'category': fields.Nested(CategorySchema),
    'media': fields.List(fields.Nested(MediaSchema), required=True, description='Ad Media list',
                         attribute='media_set'),
})


AdParser = reqparse.RequestParser()
AdParser.add_argument('title', type=parser_utils.validate_string(100, 3), required=True, location='json')
AdParser.add_argument('body', type=parser_utils.validate_string(5000, 3), required=True,  location='json')
AdParser.add_argument('category', type=parser_utils.validate_dict(['id']), required=True,  location='json')
AdParser.add_argument('media', type=parser_utils.validate_media(max_length=5, keys=['path']), required=False,
                      location='json')
