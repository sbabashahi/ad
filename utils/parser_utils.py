from utils.exceptions import CustomException


def validate_string(max_length=None, min_length=None, choices=None):
    def validate(s):
        if type(s) is not str:
            raise CustomException(detail='Must be string.')
        if min_length and len(s) < min_length:
            raise CustomException(detail='Min length is {}'.format(min_length))
        if max_length and len(s) > max_length:
            raise CustomException(detail='Max length is {}'.format(max_length))
        if choices:
            for item in choices:
                if s == item[0]:
                    break
            else:
                raise CustomException(detail='Choices are {}'.format(choices))
        return s
    return validate


def validate_int(max_length=None, min_length=None) -> int:
    def validate(i):
        i = int(i)
        if min_length and i < min_length:
            raise CustomException(detail='Min is {}'.format(min_length))
        if max_length and i > max_length:
            raise CustomException(detail='Max is {}'.format(max_length))
        return i
    return validate


def validate_dict(keys=None):
    def validate(d):
        if type(d) is not dict:
            raise CustomException(detail='Must be Dictionary.')
        if keys:
            for key in keys:
                if key not in d.keys():
                    raise CustomException(detail='{} is required'.format(key))
        return d
    return validate


def validate_media(max_length=None, min_length=None, keys=None, child_max=200):
    def validate(l):
        if type(l) is not list:
            raise CustomException(detail='Must be list.')
        if max_length and len(l) > max_length:
            raise CustomException(detail='Max length is {} and yours is {}'.format(max_length, len(l)))
        if min_length and len(l) < min_length:
            raise CustomException(detail='Min length is {} and yours is {}'.format(min_length, len(l)))
        if keys:
            for key in keys:
                for dic in l:
                    if key not in dic.keys():
                        raise CustomException(detail='{} is required'.format(key))
                    if child_max:
                        if len(dic[key]) > child_max:
                            raise CustomException(detail='{} max is {}'.format(key.title(), child_max))
        return l
    return validate
