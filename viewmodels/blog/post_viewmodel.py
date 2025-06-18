from typing import Optional
from data import db_session
from data.post import Post
from viewmodels.shared.viewmodel import ViewModelBase


class PostViewModel(ViewModelBase):
    def __init__(self, request):
        super().__init__(request)
        self.post: Optional[Post] = None
        self.title: str = ''
        self.content: str = ''
        self.error: str = ''

    async def load(self, post_id: int = None):
        if post_id:
            session = db_session.create_session()
            self.post = session.query(Post).filter(Post.id == post_id).first()
            if not self.post:
                self.error = 'Post not found'
        else:
            # For post creation
            form = await self.request.form()
            self.title = form.get('title', '').strip()
            self.content = form.get('content', '').strip()

            if not self.title:
                self.error = 'Title is required'
            elif not self.content:
                self.error = 'Content is required' 