from flask_restx import Resource

from rest import api

from user.models import User
from user.schema import LoginRegisterSchema, LoginRegisterParser
from utils.exceptions import CustomException
from utils import responses

ns = api.namespace('user', description='Login register Api')


@ns.route("/register")
class UserRegisterApi(Resource):

    @ns.doc(model=LoginRegisterSchema)
    @ns.expect(LoginRegisterParser)
    def post(self):
        """
        Register user

            username  min 5, max 50

            password  min 5, max 50


        :return:
        """
        try:
            data = LoginRegisterParser.parse_args()
            user = User.query.filter_by(username=data['username']).first()
            if user is None:
                user = User(username=data['username'])
                user.set_password(data['password'])
                user.create()
                data = {
                    'Token': user.encode_auth_token()
                }
                return responses.SuccessResponse(data).send()
            else:
                raise CustomException(detail='A user with this data exist.')
        except CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()


@ns.route("/login")
class UserLoginApi(Resource):

    @ns.doc(model=LoginRegisterSchema)
    @ns.expect(LoginRegisterParser)
    def post(self):
        """
        Login user

            username  min 5, max 50

            password  min 5, max 50


        :return:
        """
        try:
            data = LoginRegisterParser.parse_args()
            user = User.query.filter_by(username=data['username']).first()
            if user is None:
                raise CustomException(detail='User does not exist.')
            else:
                if user.check_password(data['password']):
                    data = {
                        'Token': user.encode_auth_token()
                    }
                    return responses.SuccessResponse(data).send()
                else:
                    raise CustomException(detail='User does not exist.')
        except CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()
