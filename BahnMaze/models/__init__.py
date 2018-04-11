from .pengguna import Pengguna
from .profile import Profile


def includeme(config):
    config.register_model(__name__)
