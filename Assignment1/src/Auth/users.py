class User:
    users = {}

    @classmethod
    def createUser(cls, name, pwd):
        cls.users[name] = pwd
        