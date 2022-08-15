class RootException(Exception):

    def __init__(self, detail):
        self.detail = detail

    def get_detail(self):
        return self.detail
