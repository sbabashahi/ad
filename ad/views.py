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


@ad.route("/list")
class AdListApi(Resource):

    @ad.doc(model=AdSchema)
    def get(self):
        """
        List of Ads

        with pagination index default 0, size default 20

        query by search on title and body

        category id of category

        :return:
        """
        arg = dict(request.args)
        index, size = handle_pagination(arg)
        ads = Ad.query.filter_by(is_deleted=False).all()
        total = len(ads)
        return responses.SuccessResponse(marshal_list(ads[index:size], AdSchema), index=index, total=total).send()


@ad.route("/")
class AdCreateApi(Resource):

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
        data = AdParser.parse_args()
        data['category'] = Category.query.get(data['category']['id'])
        if not data['category']:
            raise CustomException(detail='Category does not exist.')
        media = None
        if data.get('media'):
            media = data.pop('media')
        data['user'] = g.user
        ad = Ad(**data).create()
        if media:
            for item in media:
                ad.media_set.append(Media(path=item['path']))
        ad.save()
        return responses.SuccessResponse(marshal(ad, AdSchema)).send()


@ad.route("/<id>")
class AdApi(Resource):

    @ad.doc(model=AdSchema)
    def get(self, id):
        """
        Get ad details by id
        :param id:
        :return:
        """
        ad = Ad.query.get(id)
        if ad is None or ad.is_deleted:
            raise CustomException(detail='Ad does not exist.')
        return responses.SuccessResponse(marshal(ad, AdSchema)).send()

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
        data = AdParser.parse_args()
        import pdb;pdb.set_trace()
        ad = Ad.query.get(id)
        if ad is None or ad.is_deleted:
            raise CustomException(detail='Ad does not exist.')

        if ad.user != g.user:
            raise CustomException(detail='No permission.', code=403)

        if data.get('category', None) and ad.category.id != data['category']['id']:
            category = Category.query.get(data['category']['id'])
            if category:
                ad.category = category
            else:
                raise CustomException(detail='Category does not exist.')

        if data.get('title', None) and ad.title != data['title']:
            ad.title = data['title']

        if data.get('body', None) and ad.body != data['body']:
            ad.body = data['body']

        if data.get('media'):
            for media_data in data['media']:
                if media_data.get('id', None) is None:
                    ad.media_set.append(Media(path=media_data['path']))
        ad.save()
        return responses.SuccessResponse(marshal(ad, AdSchema)).send()

    @auth_required
    def delete(self, id):
        """
        Delete project

        Soft delete

        :param id:
        :return:
        """
        ad = Ad.query.get(id)
        if ad is None or ad.is_deleted:
            raise CustomException(detail='Ad does not exist.')

        if ad.user != g.user:
            raise CustomException(detail='No permission.', code=403)
        ad.is_deleted = True
        ad.save()
        return responses.SuccessResponse(status=204).send()
