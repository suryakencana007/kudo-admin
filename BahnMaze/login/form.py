import colander
from baka import log

from BahnMaze import form


@colander.deferred
def username_validator(node, kw):
    request = kw.get('request')

    def validator(_node, value):
        User = request.find_model('pengguna')
        user = User.get_by_username(request.db, value)
        if not user:
            raise colander.Invalid(
                _node,
                u'Username tidak ditemukan',
            )
    return colander.All(colander.Length(max=32), validator,)


@colander.deferred
def email_validator(node, kw):
    request = kw.get('request')

    def validator(_node, value):
        User = request.find_model('pengguna')
        user = User.get_by_email(request.db, value)
        if value and not user:
            raise colander.Invalid(
                _node,
                u'Email tidak ditemukan',
            )
    return colander.All(colander.Email(), validator,)


@colander.deferred
def password_validator(node, kw):
    request = kw.get('request')

    def validator(_node, value):
        User = request.find_model('pengguna')
        user = User.get_by_email(request.db, request.params.get('email'))
        if user and not User.verify_password(value, user.password):
            raise colander.Invalid(
                _node,
                u'Password is mistaken',
            )
    return colander.All(colander.Length(min=6, max=128), validator,)


class _LoginSchema(form.CSRFSchema):
    email = colander.SchemaNode(
        colander.String(),
        validator=email_validator
    )
    password = colander.SchemaNode(
        colander.String(),
        validator=password_validator
    )


class LoginForm(form.BaseForm):
    _schema = _LoginSchema

    def submit(self, obj=None):
        User = self.request.find_model('pengguna')
        return User.get_by_email(self.request.db, self._controls.get('email'))

