from baka import log
from baka.response import JSONAPIResponse
from sqlalchemy.exc import SQLAlchemyError

from BahnMaze.app import app
from BahnMaze.jsonapi import QueryBuilder
from BahnMaze.login.factory import LoginFactory
from BahnMaze.user.form import UserEditForm, UserAddForm, UserForgotForm
from BahnMaze.utils import MAX_LIMIT, DEFAULT_LIMIT, mapper_alchemy


@app.resource(
    '/users',
    route_name='daftar_pengguna'
)
class UserList(LoginFactory):

    def __init__(self, request):
        self._title = 'Daftar Pengguna'
        self.user = request.find_model('pengguna')


@UserList.GET(renderer='BahnMaze:user/templates/list.html', permission='read')
def daftar_pengguna(page, request):
    return {'title': page._title}


@UserList.POST()
def api_daftar_pengguna(page, request):
    data = {}
    with JSONAPIResponse(request.response) as resp:
        _in = u'Failed'
        code, status = JSONAPIResponse.BAD_REQUEST
        if page.user:
            QueryBuilder.max_limit = MAX_LIMIT
            QueryBuilder.default_limit = DEFAULT_LIMIT
            query_builder = QueryBuilder(request, page.user)
            query, pagination = query_builder.get_collection_query()
            rows = query.all()
            data = [mapper_alchemy(
                page.user, row)
                for row in rows]

            _in = u'Success'
            code, status = JSONAPIResponse.OK

    return resp.to_json(
        _in, code=code,
        status=status,
        data=data,
        total=pagination.get('total', 0))


@app.resource(
    '/user',
    route_name='tambah_pengguna'
)
class UserTambah(object):
    def __init__(self, request):
        self._title = 'Form Tambah Pengguna'
        self.session = request.db
        self.user = request.find_model('pengguna')


@UserTambah.GET(renderer='BahnMaze:user/templates/register.html')
def tambah_pengguna(page, request):
    return {
        'title': page._title
    }


@UserTambah.POST()
def api_tambah_pengguna(page, request):
    form = UserAddForm(request)
    if form.validate():
        user = form.submit()
        request.db.add(user)

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


@app.resource(
    '/user/{uid:.*}/forgot',
    route_name='form_lupa_sandi'
)
class UserForgot(object):
    def __init__(self, request):
        self._title = 'Form Lupa Kata Sandi'
        self.uuid = request.matchdict.get('uid')
        self.session = request.db
        self.model = request.find_model('pengguna')
        self.user = self.session.query(self.model).filter_by(
            uid=self.uuid).first()
        self.result = {
            'title': self._title,
            'action': request.route_url('form_lupa_sandi', uid=self.uuid),
        }


@UserForgot.GET(renderer='BahnMaze:user/templates/forgot.html')
def lupa_sandi(page, request):
    return {
        'uid': page.uuid,
        'title': page._title,
        'username': page.user.username
    }


@UserForgot.POST()
def api_simpan_lupa_sandi(page, request):
    form = UserForgotForm(request)
    if form.validate():
        user = form.submit(page.user)
        request.db.add(user)

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


@app.resource(
    '/user/{uid:.*}',
    route_name='form_pengguna'
)
class UserForm(object):
    def __init__(self, request):
        self._title = 'Form Pengguna'
        self.session = request.db
        self.user = request.find_model('pengguna')
        self.uuid = request.matchdict.get('uid')
        self.result = {
            'title': self._title,
            'action': request.route_url('form_pengguna', uid=self.uuid),
        }


@UserForm.GET(renderer='BahnMaze:user/templates/update.html')
def lihat_pengguna(page, request):
    try:
        data = {
            'error': 'Data Pengguna tidak ditemukan'
        }
        user = page.session.query(page.user).filter_by(
            uid=page.uuid).first()

        if user:
            data = mapper_alchemy(page.user, user)

        page.result.update({
            **data
        })
    except SQLAlchemyError as e:
        log.info(e)
        page.result.update({
            'error': 'Pengguna ID tidak ada'
        })

    return page.result


@UserForm.POST()
def api_simpan_pengguna(page, request):
    form = UserEditForm(request)
    if form.validate():
        user = form.submit()
        request.db.add(user)

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


def includeme(config):
    pass
