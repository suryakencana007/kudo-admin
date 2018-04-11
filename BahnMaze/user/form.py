import colander
from baka import log

from BahnMaze import form


@colander.deferred
def username_validator(node, kw):
    request = kw.get('request')

    def validator(_node, value):
        User = request.find_model('pengguna')
        user = User.get_by_username(request.db, value)
        if user and str(user.uid) != request.params.get('uid'):
            raise colander.Invalid(
                _node,
                u'User with the same username exists',
            )
    return colander.All(colander.Length(max=32), validator,)


@colander.deferred
def email_validator(node, kw):
    request = kw.get('request')

    def validator(_node, value):
        User = request.find_model('pengguna')
        user = User.get_by_email(request.db, value)
        if user and str(user.uid) != request.params.get('uid'):
            raise colander.Invalid(
                _node,
                u'User with the same email exists',
            )
    return colander.All(colander.Email(), validator,)


@colander.deferred
def employee_validator(node, kw):
    request = kw.get('request')

    def validator(_node, value):
        User = request.find_model('pengguna')
        user = User.by_employee_id(value)
        if user and str(user.uid) != request.params.get('uid'):
            raise colander.Invalid(
                _node,
                u'User for this employee already exists',
            )
    return colander.All(validator,)


@colander.deferred
def password_validator(node, kw):
    request = kw.get('request')

    def validator(_node, value):
        if value and request.params.get('password_confirm') != value:
            raise colander.Invalid(
                _node,
                u'Password and confirm is not equal',
            )
    return colander.All(colander.Length(min=6, max=128), validator,)


@colander.deferred
def password_old_validator(node, kw):
    request = kw.get('request')

    def validator(_node, value):
        log.info(value)
        User = request.find_model('pengguna')
        user = request.db.query(User).filter_by(
            uid=request.params.get('uid')).first()
        if not User.verify_password(value, user.password):
            raise colander.Invalid(
                _node,
                u'Password is mistaken',
            )
    return colander.All(colander.Length(min=6, max=128), validator,)


class _UserEditSchema(form.CSRFSchema):
    username = colander.SchemaNode(
        colander.String(),
        validator=username_validator
    )
    email = colander.SchemaNode(
        colander.String(),
        validator=email_validator
    )


class _PasswordSchema(form.CSRFSchema):
    password = colander.SchemaNode(
        colander.String(),
        validator=password_validator
    )
    password_confirm = colander.SchemaNode(
        colander.String()
    )


class _UserForgotSchema(_PasswordSchema):
    password_old = colander.SchemaNode(
        colander.String(),
        validator=password_old_validator
    )


class _UserAddSchema(
    _UserEditSchema,
    _PasswordSchema):
    pass


class _UserAddForm(form.BaseForm):

    def submit(self, user=None):
        if not user:
            user = self.request.find_model('pengguna')()

        user.username = self._controls.get('username')
        user.email = self._controls.get('email')
        if self._controls.get('password'):
            user.password = self._controls.get('password').strip()
        return user


class UserAddForm(_UserAddForm):
    _schema = _UserAddSchema


class _UserEditForm(form.BaseForm):
    def submit(self, user=None):
        if not user:
            user = self.request.find_model('pengguna')()

        user.username = self._controls.get('username')
        user.email = self._controls.get('email')
        return user


class UserEditForm(_UserEditForm):
    _schema = _UserEditSchema


class _UserForgotForm(form.BaseForm):
    def submit(self, user=None):
        if not user:
            user = self.request.find_model('pengguna')()

        if self._controls.get('password'):
            user.password = self._controls.get('password').strip()
        return user


class UserForgotForm(_UserForgotForm):
    _schema = _UserForgotSchema
