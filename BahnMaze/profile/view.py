from baka import log
from BahnMaze.app import app
from BahnMaze.login.factory import LoginFactory
from BahnMaze.utils import mapper_alchemy


@app.resource(
    '/profile/{uid:.*}',
    route_name='profile_page'
)
class ProfilePage(LoginFactory):
    def __init__(self, request):
        self._title = 'Profile'
        self.profile = request.find_model('profile')
        self.user = request.find_model('pengguna')


@ProfilePage.GET(renderer='BahnMaze:profile/templates/form.html')
def profile_get(page, request):
    data = {}
    s = request.db
    user = s.query(page.user).filter_by(
        uid=request.matchdict.get('uid')).first()

    profile = user.profile
    if profile:
        data = mapper_alchemy(page.profile, profile)
    log.info(user.username)
    log.info(profile)
    return {
        'title': page._title,
        'action': request.route_url('profile_page', uid=user.uid),
        **data
    }


@ProfilePage.POST()
def profile_post(page, request):
    s = request.db

    user = s.query(page.user).filter_by(
        uid=request.matchdict.get('uid')).first()

    params = request.params

    log.info(params)
    profile = page.profile()
    profile.display_name = params.get('display_name')
    profile.first_name = params.get('first_name')
    profile.last_name = params.get('last_name')
    # profile.description = 'Hahahahaha'
    profile.user = user
    log.info(request.matchdict.get('uid'))
    s.add(profile)
    return { 'title': page._title }


def includeme(config):
    pass
