from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget

from BahnMaze.app import app
from BahnMaze.login.form import LoginForm


@app.resource(
    '/login',
    route_name='login_pengguna'
)
class LoginPengguna(object):
    def __init__(self, request):
        self._title = 'Login Pengguna'
        self.user = request.find_model('pengguna')


@LoginPengguna.GET(renderer='BahnMaze:login/templates/login.html')
def login_pengguna(page, request):
    if request.authenticated_userid:
        return app.redirect(request.route_url('daftar_pengguna'))

    return {'title': page._title}


@LoginPengguna.POST()
def api_login_pengguna(page, request):
    form = LoginForm(request)
    if form.validate():
        user = form.submit()

        request.response.headers = remember(request, user.email)

        return {
            'redirect': '/users',
            'success_message': u'Saved',
            'response': 0
        }
    else:
        return {
            'error_message': u'Please, check errors',
            'errors': form.errors
        }


@app.route('/logout')
def logout_pengguna(request):
    return HTTPFound(
        location=request.route_url('login_pengguna'),
        headers=forget(request)
    )


def forbidden(request):
    return app.redirect(request.route_url('login_pengguna'))

def includeme(config):
    config.add_forbidden_view(forbidden)
