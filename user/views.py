from flask import request, g
from flask_restx import Resource

from rest import api
from ad.schema import AdSchema
from user.models import User
from user.schema import LoginRegisterSchema, LoginRegisterParser
from utils import responses
from utils.exceptions import CustomException
from utils.middleware import auth_required
from utils.utils import handle_pagination, marshal_list

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
            user = User.query.get(username=data['username'])
            if user is None:
                user = User(username=data['username'])
                user.set_password(data['password'])
                user.create()
                data = {
                    'token': user.encode_auth_token()
                }
                return responses.SuccessResponse(data, status=201).send()
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
            user = User.query.get(username=data['username'])
            if user is None:
                raise CustomException(detail='User does not exist.')
            else:
                if user.check_password(data['password']):
                    data = {
                        'token': user.encode_auth_token()
                    }
                    return responses.SuccessResponse(data).send()
                else:
                    raise CustomException(detail='username or password is incorrect.')
        except CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()


@ns.route("/my_ads")
class CategoryListApi(Resource):

    @auth_required
    @ns.doc(model=AdSchema)
    def get(self):
        """
        List of categories

            with pagination index default 0, size default 20

        :return:
        """
        try:
            arg = dict(request.args)
            index, size = handle_pagination(arg)
            my_ads = g.user.my_ads()
            total = len(my_ads)
            return responses.SuccessResponse(marshal_list(my_ads[index:size], AdSchema),
                                             index=index, total=total).send()
        except CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()
