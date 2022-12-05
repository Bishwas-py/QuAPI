from datetime import datetime

from pony import orm

from core.initializers.database import db


class User(db.Entity):
    _table_ = 'users'
    id = orm.PrimaryKey(int, auto=True)
    username = orm.Required(str, unique=True)
    password = orm.Required(str)

    first_name = orm.Required(str)
    last_name = orm.Required(str)
    email = orm.Required(str, unique=True)

    is_verified = orm.Required(bool, default=False)
    is_active = orm.Required(bool, default=True)
    is_admin = orm.Required(bool, default=False)

    profile = orm.Required('Profile', reverse='user')

    created_at = orm.Required(datetime, default=datetime.utcnow)
    updated_at = orm.Required(datetime, default=datetime.utcnow)

    orm.composite_key(username, email)


class Profile(db.Entity):
    _table_ = 'profiles'
    id = orm.PrimaryKey(int, auto=True)
    user = orm.Required(User)
    bio = orm.Optional(str)
    avatar = orm.Optional(str)

    created_at = orm.Required(datetime, default=datetime.utcnow)
    updated_at = orm.Required(datetime, default=datetime.utcnow)

    orm.composite_key(user, bio, avatar)
