from flask import g

from category.models import Category
from setting.database import db
from utils.model import BaseModel
from utils.exceptions import CustomException
from utils.utils import now_time


class Media(BaseModel):
    __tablename__ = 'media'
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), nullable=False)
    ad_id = db.Column(db.Integer, db.ForeignKey('ad.id'), nullable=False)
    ad = db.relationship('Ad', backref=db.backref('media_set', lazy=True))

    def __str__(self):
        return ''.join(['Media: ', self.title])


class Ad(BaseModel):
    __tablename__ = 'ad'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created = db.Column(db.Integer, nullable=False, default=now_time)
    is_deleted = db.Column(db.Boolean, default=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('ads', lazy=True))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('ad_set', lazy=True))

    def __str__(self):
        return ''.join(['Ad: ', self.title])

    def has_permission(self):
        if self.user != g.user:
            raise CustomException(detail='No permission.', code=403)

    def delete(self):
        self.is_deleted = True
        self.save()

    def update(self, data):
        if data.get('category', None) and self.category.id != data['category']['id']:
            category = Category.query.get(data['category']['id'])
            if category:
                self.category = category
            else:
                raise CustomException(detail='Category does not exist.')

        if data.get('title', None) and self.title != data['title']:
            self.title = data['title']

        if data.get('body', None) and self.body != data['body']:
            self.body = data['body']

        if data.get('media'):
            for media_data in data['media']:
                if media_data.get('id', None) is None:
                    self.media_set.append(Media(path=media_data['path']))
        self.save()
