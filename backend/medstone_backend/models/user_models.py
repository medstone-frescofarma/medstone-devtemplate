import datetime

import bcrypt
from sqlalchemy import Table, Column, ForeignKey, Boolean, Integer, String, Unicode, UnicodeText, DateTime
from sqlalchemy.orm import relationship, backref, object_session

from medstone_backend.db.base_class import Base
from medstone_backend.models.util import TimestampMixin, EmailType
from medstone_backend.models import location_models


# pivot table between Authorization and Role
authorization_role = Table('authorization_role', Base.metadata,
    Column('authorization_id', Integer, ForeignKey('authorization.id')),
    Column('role_id', Integer, ForeignKey('role.id'))
)

# pivot table between User and Role
user_role = Table('user_role', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('role_id', Integer, ForeignKey('role.id'))
)

class Authorization(Base, TimestampMixin):
    '''Stores the authorizations'''
    __tablename__ = 'authorization'

    # primary key
    id      = Column(Integer, primary_key=True, autoincrement=True)

    # object properties
    name        = Column(String, nullable=False, unique=True)
    description = Column(UnicodeText, nullable=True)

    # relationships
    roles   = relationship('Role', secondary=authorization_role, back_populates='_authorizations')


class Role(Base, TimestampMixin):
    """Stores the roles we have"""
    __tablename__ = 'role'
    # primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # forein keys
    parent_id = Column(Integer, ForeignKey('role.id'), nullable=True)

    # object properties
    name = Column(UnicodeText, nullable=False, unique=True)
    description = Column(UnicodeText, nullable=False)

    # relationships
    children = relationship("Role", lazy='joined', join_depth=0, backref=backref('parent', remote_side=[id]))
    users = relationship('User', secondary=user_role, back_populates='_roles')
    _authorizations = relationship('Authorization', secondary=authorization_role, back_populates='roles')
    
    @property
    def authorizations(self):
        return self._authorizations

    @authorizations.setter
    def authorizations(self, new_authorization_ids):
        db = object_session(self)
        if type(new_authorization_ids) == list:
            # either list of ints of list of dicts expected as input
            new_authorization_ids = [i if type(i) == int else i['id'] for i in new_authorization_ids]
            # set the new authorizations on the object
            self._authorizations = db.query(
                self.__class__._authorizations.property.mapper.class_
            ).filter(
                self.__class__._authorizations.property.mapper.class_.id.in_(new_authorization_ids)
            ).all()


class User(Base, TimestampMixin):
    """Model for storing subcategories under a category"""
    __tablename__ = 'user'

    # primary key
    id              = Column(Integer, primary_key=True, autoincrement=True)

    # object properties
    username        = Column(UnicodeText, nullable=False, unique=True)
    name            = Column(UnicodeText, nullable=True)
    email           = Column(EmailType, nullable=False, unique=True)
    password_hash   = Column(Unicode(255), nullable=False)
    is_active       = Column(Boolean, nullable=False, server_default='true')
    is_admin        = Column(Boolean, nullable=False, server_default='false')
    totp_secret     = Column(String, nullable=True)
    last_login      = Column(DateTime(timezone=True), nullable=True)

    # set the default status of a user to not-two-factor authenticated
    is_2fa_authenticated = False

    # relationships
    _roles = relationship(
        'Role', 
        secondary='user_role',
        lazy='joined',
        back_populates='users'
    )

    @property
    def roles(self):
        return self._roles

    @roles.setter
    def roles(self, new_role_ids):
        db = object_session(self)
        if type(new_role_ids) == list:
            # either list of ints of list of dicts expected as input
            new_role_ids = [i if type(i) == int else i['id'] for i in new_role_ids]
            # set the new roles on the object
            self._roles = db.query(
                self.__class__._roles.property.mapper.class_
            ).filter(
                self.__class__._roles.property.mapper.class_.id.in_(new_role_ids)
            ).all()

    @property
    def password(self):
        raise AttributeError('password not readable')

    @property
    def has_2fa(self):
        return self.totp_secret != None

    @password.setter
    def password(self, password):
        # bcrypt expects bytes as input
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        # bcrypt expects bytes as input
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
