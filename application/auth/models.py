"""Users and Roles Database Model Definitions"""

from flask_admin.contrib.sqla import ModelView
from flask_security import UserMixin, RoleMixin, current_user, utils
from wtforms.fields import PasswordField

from application.database import DB

ROLES_USERS = DB.Table(
    'roles_users',
    DB.Column('user_id', DB.Integer(), DB.ForeignKey('user.id')),
    DB.Column('role_id', DB.Integer(), DB.ForeignKey('role.id')),
)


class Role(DB.Model, RoleMixin):
    """Roles / Permissions Groups"""
    id = DB.Column(DB.Integer(), primary_key=True)
    name = DB.Column(DB.String(80), unique=True)
    description = DB.Column(DB.String(255))

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Role {self.name}>"


class RoleAdmin(ModelView):
    """Flask-admin ModelView for the Role model"""
    def is_accessible(self):
        """Make sure only admins can see this"""
        return current_user.has_role('admin')


class User(DB.Model, UserMixin):
    """Platform User"""
    id = DB.Column(DB.Integer(), primary_key=True)
    email = DB.Column(DB.String(255), unique=True)
    password = DB.Column(DB.String(255))
    active = DB.Column(DB.Boolean())
    confirmed_at = DB.Column(DB.DateTime())
    last_login_at = DB.Column(DB.DateTime())
    current_login_at = DB.Column(DB.DateTime())
    last_login_ip = DB.Column(DB.String(15))
    current_login_ip = DB.Column(DB.String(15))
    login_count = DB.Column(DB.Integer())
    roles = DB.relationship(
        'Role',
        secondary=ROLES_USERS,
        backref=DB.backref('users', lazy='dynamic')
    )

    def __str__(self):
        return self.email

    def __repr__(self):
        return f"<User {self.email}>"

class UserAdmin(ModelView):
    """Flask-admin ModelView for the User model"""
    column_exclude_list = ('password',)
    form_excluded_columns = ('password',)
    column_auto_select_related = True

    def is_accessible(self):
        """Make sure only admins can see this"""
        return current_user.has_role('admin')

    def scaffold_form(self):
        """
        On the form for creating or editing a User,
        don't display a field corresponding to the model's password field.
        There are two reasons for this.
        First, we want to encrypt the password before storing in the database.
        Second, we want to use a password field rather than a regular text field.
        """
        # Start with the standard form as provided by Flask-Admin.
        form_class = super(UserAdmin, self).scaffold_form()
        # Add a password field, naming it "password2" and labeling it "New Password".
        form_class.password2 = PasswordField('New Password')
        return form_class

    def on_model_change(self, form, model, is_created):
        """This callback executes when the user saves a User"""
        # If the password field isn't blank...
        if len(model.password2) > 0:
            model.password = utils.encrypt_password(model.password2)
