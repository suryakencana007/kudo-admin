import datetime


import sqlalchemy

from baka_tenshi import DB, Model, util, verify_password
from baka_tenshi.type import GUID, PasswordType
from sqlalchemy.ext.hybrid import hybrid_property

EMAIL_MAX_LENGTH = 100


class Pengguna(Model):

    __tablename__ = u'pengguna'

    prefix = u'usr-'

    # Normalised user identifier
    uid = DB.Column('uid', GUID())

    #: Akun for login
    _username = DB.Column('nama_pengguna',
                          DB.VARCHAR(140),
                          nullable=False,
                          unique=True)

    email = DB.Column('email_pengguna', DB.VARCHAR(EMAIL_MAX_LENGTH), nullable=False)

    registered_date = DB.Column('tgl_ubah_kunci', DB.TIMESTAMP(timezone=False),
                                default=datetime.datetime.utcnow,
                                server_default=DB.func.now(),
                                nullable=False)

    _password = DB.Column('kunci_pengguna', PasswordType(), nullable=False)

    password_updated = DB.Column('kunci_ubah_pengguna', DB.DateTime(), nullable=True)

    profile = DB.relationship('Profile', uselist=False, back_populates="user")

    def __init__(self):
        self.uid = util.guid()

    @hybrid_property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value
        self.password_updated = datetime.datetime.utcnow()

    @classmethod
    def get_by_email(cls, session, email):
        """Fetch a user by email address."""
        return session.query(cls).filter(
            sqlalchemy.func.lower(cls.email) == email.lower()
        ).first()

    @classmethod
    def get_by_username(cls, session, username):
        """Fetch a user by username."""
        return session.query(cls).filter(
            cls.username == username
        ).first()

    @classmethod
    def verify_password(cls, password, hash):
        return verify_password(password, hash)
