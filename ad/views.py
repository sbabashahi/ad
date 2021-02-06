from flask import request, g
from flask_restx import Resource, marshal


from rest import api
from utils.middleware import auth_required
from category.models import Category
from ad.models import Ad, Media
from ad.schema import AdParser, AdSchema
from utils.utils import handle_pagination, marshal_list
from utils import responses
from utils.exceptions import CustomException

ad = api.namespace('ad', description='Ad Api')


@ad.route("/")
class AdApi(Resource):

    @ad.doc(model=AdSchema)
    def get(self):
        """
        List of Ads

        with pagination index default 0, size default 20

        query by search on title and body

        category id of category

        :return:
        """
        try:
            arg = dict(request.args)
            index, size = handle_pagination(arg)
            ads = Ad.query.filter_by(is_deleted=False).all()
            total = len(ads)
            return responses.SuccessResponse(marshal_list(ads[index:size], AdSchema), index=index, total=total).send()
        except CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()

    @auth_required
    @ad.doc(model=AdSchema)
    @ad.expect(AdParser)
    def post(self):
        """
        Create Ad

            title  min 3, max 100

            body  min 3, max 100

            category  {'id': id of category}

            media  [{'path': 'path of media'}] max 5


        :return:
        """
        try:
            data = AdParser.parse_args()
            data['category'] = Category.query.get(data['category']['id'])
            if not data['category']:
                raise CustomException(detail='Category does not exist.')
            media = data.pop('media')
            data['user'] = g.user
            ad_item = Ad(**data).create()
            if media:
                for item in media:
                    ad_item.media_set.append(Media(path=item['path']))
            ad_item.save()
            return responses.SuccessResponse(marshal(ad_item, AdSchema), status=201).send()
        except CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()


@ad.route("/<id>")
class AdRUDApi(Resource):

    @ad.doc(model=AdSchema)
    def get(self, id):
        """
        Get ad details by id
        :param id:
        :return:
        """
        try:
            ad_item = Ad.query.get(id)
            if ad_item is None or ad_item.is_deleted:
                raise CustomException(detail='Ad does not exist.')
            return responses.SuccessResponse(marshal(ad_item, AdSchema)).send()
        except CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()

    @auth_required
    @ad.expect(AdSchema)
    def put(self, id):
        """
        Update ad details by id

            title  min 3, max 100

            body  min 3, max 100

            category  {'id': id of category}

            media  [{'path': 'path of media', 'id': 'id of gallery'}] max 5  id is optional for checking previous created

        :param id:
        :return:
        """
        try:
            data = AdParser.parse_args()
            ad_item = Ad.query.get(id)
            if ad_item is None or ad_item.is_deleted:
                raise CustomException(detail='Ad does not exist.')

            ad_item.has_permission()
            ad_item.update(data)
            return responses.SuccessResponse(marshal(ad_item, AdSchema)).send()
        except CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()

    @auth_required
    def delete(self, id):
        """
        Delete project

        Soft delete

        :param id:
        :return:
        """
        try:
            ad_item = Ad.query.get(id)
            if ad_item is None or ad_item.is_deleted:
                raise CustomException(detail='Ad does not exist.')
            ad_item.has_permission()
            ad_item.delete()
            return responses.SuccessResponse(status=204).send()
        except CustomException as e:
            return responses.ErrorResponse(message=e.detail, status=e.status_code).send()
