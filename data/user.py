import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.modelbase import SqlAlchemyBase
from sqlalchemy.orm import Mapped
from data.post import Post
from data.comment import Comment


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name: str = sa.Column(sa.String)
    email: str = sa.Column(sa.String, index=True, unique=True)
    hash_password: str = sa.Column(sa.String)
    created_date: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    last_login: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    profile_image_url: str = sa.Column(sa.String)

    # New relationships
    posts: Mapped[list["Post"]] = orm.relationship("Post", back_populates='author')
    comments: Mapped[list["Comment"]] = orm.relationship("Comment", back_populates='author')

