from .user import User


class LoggedInUser(User):

    email: str
    password: str

    def __init__(self, context, email=None, password=None):
        super().__init__(context, email, password)
        self.register()
        self.confirm()
