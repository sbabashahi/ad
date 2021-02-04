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
        data = LoginRegisterParser.parse_args()
        user = User.query.filter_by(username=data['username']).first()
        if user is None:
            user = User(username=data['username'])
            user.set_password(data['password'])
            user.create()
            data = {
                'Token': ''
            }
            return responses.SuccessResponse(data).send()
        else:
            raise CustomException(detail='A user with this data exist.')
