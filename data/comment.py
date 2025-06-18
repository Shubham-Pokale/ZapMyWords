import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm
from data.modelbase import SqlAlchemyBase
from sqlalchemy.orm import Mapped


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    content: str = sa.Column(sa.Text, nullable=False)
    created_date: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now)

    # Relationships
    author_id: int = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    post_id: int = sa.Column(sa.Integer, sa.ForeignKey('posts.id'))
    parent_id: int = sa.Column(sa.Integer, sa.ForeignKey('comments.id'), nullable=True)

    author: Mapped["User"] = orm.relationship('User', back_populates='comments')
    post: Mapped["Post"] = orm.relationship('Post', back_populates='comments')
    replies: Mapped[list["Comment"]] = orm.relationship('Comment', backref=orm.backref('parent', remote_side=[id]))

    def __repr__(self):
        return f'<Comment {self.id}>' 