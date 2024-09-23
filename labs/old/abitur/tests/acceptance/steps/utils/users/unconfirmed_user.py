from .user import User


class UnconfirmedUser(User):

    def __init__(self, context, email=None, password=None):
        super(UnconfirmedUser, self).__init__(context, email, password)
        self.register()