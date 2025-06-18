import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.modelbase import SqlAlchemyBase
from sqlalchemy.orm import Mapped


class Post(SqlAlchemyBase):
    __tablename__ = 'posts'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    title: str = sa.Column(sa.String, nullable=False)
    content: str = sa.Column(sa.Text, nullable=False)
    created_date: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now)
    updated_date: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    published_date: datetime.datetime = sa.Column(sa.DateTime, nullable=True)
    status: str = sa.Column(sa.String, default='draft')  # draft or published
    slug: str = sa.Column(sa.String, unique=True, index=True)

    # Relationships
    author_id: int = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    author: Mapped["User"] = orm.relationship('User', back_populates='posts')
    comments: Mapped[list["Comment"]] = orm.relationship("Comment", back_populates='post')

    def __repr__(self):
        return f'<Post {self.title}>' 