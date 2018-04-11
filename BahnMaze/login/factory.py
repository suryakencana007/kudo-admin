from pyramid.security import Allow, Everyone, Authenticated


class LoginFactory(object):

    def __acl__(self):
        acl = [(Allow, Everyone, 'view'),
               (Allow, Authenticated, 'read'),
               (Allow, Authenticated, 'create'),
               (Allow, Authenticated, 'edit'), ]

        return acl

    def __init__(self, request):
        self.request = request
