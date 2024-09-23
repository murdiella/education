from .logged_in_user import LoggedInUser


class LoggedOutUser(LoggedInUser):

    def __init__(self, context, email=None, password=None):
        super(LoggedOutUser, self).__init__(context, email, password)
        self.logout()
