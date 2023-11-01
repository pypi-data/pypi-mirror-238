# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,E0402,E0602,C0411,C0412,C0413,W0404,W0105,R0903
# pylint: disable=R0915,R0912,E1102


"users"


from .disk   import sync
from .object import Default


class NoUser(Exception):

    pass


class User(Default):

    def __init__(self):
        Default.__init__(self)
        self.user = ''
        self.perms = []


class Users:

    @staticmethod
    def allowed(origin, perm):
        perm = perm.upper()
        user = Users.get_user(origin)
        val = False
        if user and perm in user.perms:
            val = True
        return val

    @staticmethod
    def delete(origin, perm):
        res = False
        for user in Users.get_users(origin):
            try:
                user.perms.remove(perm)
                sync(user)
                res = True
            except ValueError:
                pass
        return res

    @staticmethod
    def get_users(origin=''):
        selector = {'user': origin}
        return [x[1] for x in find('user', selector)]

    @staticmethod
    def get_user(origin):
        users = list(Users.get_users(origin))
        res = None
        if users:
            res = users[-1]
        return res

    @staticmethod
    def perm(origin, permission):
        user = Users.get_user(origin)
        if not user:
            raise NoUser(origin)
        if permission.upper() not in user.perms:
            user.perms.append(permission.upper())
            sync(user)
        return user
