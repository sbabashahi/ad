class CustomException(Exception):

    def __init__(self, detail, code=400):
        self.detail = detail
        self.status_code = code

    def __str__(self):
        return self.detail
