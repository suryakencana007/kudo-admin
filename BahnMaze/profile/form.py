import colander

from BahnMaze import form


class _ProfileAddSchema(form.CSRFSchema):
    pass
    # first = colander.SchemaNode(
    #     colander.String(),
    #     validator=colander.All(colander.Length(min=3, max=128))
    # )
    # last = colander.SchemaNode(
    #     colander.String(),
    #     validator=colander.All(colander.Length(min=3, max=128))
    # )
    # email = colander.SchemaNode(
    #     colander.String(),
    #     validator=email_validator
    # )
    # confirm_email = colander.SchemaNode(
    #     colander.String(),
    #     validator=confirm_email_validator
    # )
    # password = colander.SchemaNode(
    #     colander.String(),
    #     validator=colander.All(colander.Length(min=6, max=128))
    # )


class _ProfileForm(form.BaseForm):

    def submit(self, user=None):
        pass
        # if not user:
        #     user = self.request.find_model('membership.user')()
        #
        # log.debug(user)
        #
        # user.username = '.'.join([
        #     self._controls.get('first'),
        #     self._controls.get('last'),
        #     helper.generate_random_string(8)])
        # user.email = self._controls.get('email')
        # user.status = u'member'
        # if self._controls.get('password'):
        #     user.password = self._controls.get('password')
        # return user


class ProfileAddForm(_ProfileForm):
    # _schema = _ProfileAddSchema
    pass