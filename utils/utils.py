import time
from uuid import uuid4

from flask_restx import marshal


def now_time():
    return round(time.time())


def create_jwt_secret():
    return ''.join(str(uuid4()).split('-'))


def handle_pagination(args):
    index = int(args.pop('index', 0))
    size = int(args.pop('size', 20))
    return index, size + index


def marshal_list(list_items, model):
    decoded_list_items = []
    for item in list_items:
        decoded_list_items.append(marshal(item, model))
    return decoded_list_items
