from typing import List
from data import db_session
from data.post import Post
from viewmodels.shared.viewmodel import ViewModelBase


class BlogViewModel(ViewModelBase):
    def __init__(self, request):
        super().__init__(request)
        self.posts: List[Post] = []

    async def load(self):
        session = db_session.create_session()
        self.posts = session.query(Post).filter(Post.status == 'published').order_by(Post.created_date.desc()).all() 