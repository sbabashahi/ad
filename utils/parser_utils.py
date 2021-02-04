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
