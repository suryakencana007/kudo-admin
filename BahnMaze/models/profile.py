from baka_tenshi import Model, DB, util
from baka_tenshi.type import GUID

from .pengguna import Pengguna


class Profile(Model):

    __tablename__ = u'profile'

    prefix = u'prf-'

    # Normalised user identifier
    uid = DB.Column('uid', GUID())

    #: The display name which will be used when rendering an annotation.
    display_name = DB.Column('profile_pengguna', DB.VARCHAR(140))

    first_name = DB.Column('nama_depan', DB.VARCHAR(140))
    last_name = DB.Column('nama_belakang', DB.VARCHAR(140))

    #: A short user description/bio
    description = DB.Column('keterangan', DB.Text())

    user_id = DB.Column(DB.Integer, DB.ForeignKey(Pengguna.id))
    user = DB.relationship(Pengguna, back_populates='profile')

    def __init__(self):
        self.uid = util.guid()
