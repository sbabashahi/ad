from flask import request
from flask_restx import Resource, marshal


from rest import api
from utils.middleware import auth_required
from category.models import Category
from category.schema import CategorySchema, CategoryParser
from utils import responses
from utils.exceptions import CustomException
from utils.utils import handle_pagination, marshal_list


ca = api.namespace('category', description='Category Api')


@ca.route("/list")
class CategoryListApi(Resource):

    @ca.doc(model=CategorySchema)
    def get(self):
        """
        List of categories

        with pagination index default 0, size default 20

        :return:
        """
        try:
            arg = dict(request.args)
            index, size = handle_pagination(arg)
            categories = Category.query.all()
            total = len(categories)
            return responses.SuccessResponse(marshal_list(categories[index:size], CategorySchema),
                                             index=index, total=total).send()
        except CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()


@ca.route("/")
class CategoryCreateApi(Resource):

    @auth_required
    @ca.doc(model=CategorySchema)
    @ca.expect(CategoryParser)
    def post(self):
        """
        Create Category

            name string min_length 3, max_length 50


        :return:
        """
        try:
            data = CategoryParser.parse_args()
            category = Category(**data).create()
            return responses.SuccessResponse(marshal(category, CategorySchema)).send()
        except CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()
