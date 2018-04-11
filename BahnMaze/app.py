from baka import Baka
from baka.log import log
from baka.settings import EnvSetting, database_url
from baka_armor.config import CONFIG as armor
from baka_tenshi.config import CONFIG as tenshi
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.httpexceptions import HTTPFound
from pyramid.session import SignedCookieSessionFactory


session_factory = SignedCookieSessionFactory('itsaseekreet')
authentication_policy = AuthTktAuthenticationPolicy('itsaseekreet')
authorization_policy = ACLAuthorizationPolicy()


ENV = [
    EnvSetting('url', 'DATABASE_URL', type=database_url),
    EnvSetting('sqlalchemy.url', 'DATABASE_URL', type=database_url)
]
options = {
    'pyramid.reload_templates': True,
    'LOGGING': True,
    'validator': False,
    'secret_key': '',
    'env': ENV
}

app = Baka(
    __name__,
    **options)

app.config.set_session_factory(session_factory)
app.config.set_authentication_policy(authentication_policy)
app.config.set_authorization_policy(authorization_policy)


# untuk validator config file
app.config.add_config_validator(armor)
app.config.add_config_validator(tenshi)
app.include('baka_tenshi')
app.include('baka_armor')


# modular aplikasi
app.include('BahnMaze.models')
app.include('BahnMaze.login')
app.include('BahnMaze.user')
app.include('BahnMaze.profile')

@app.route('/')
def HomePage(request):
    return HTTPFound(
        location=request.route_url('daftar_pengguna')
    )