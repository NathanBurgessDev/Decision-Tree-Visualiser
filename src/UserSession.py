class UserSession(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(UserSession, cls).__new__(cls)
        return cls.instance

    modelInformation = {}
