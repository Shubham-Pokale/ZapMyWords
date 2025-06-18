import fastapi
from fastapi_chameleon import template
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette import status

from data import db_session
from data.post import Post
from viewmodels.blog.blog_viewmodel import BlogViewModel
from viewmodels.blog.post_viewmodel import PostViewModel
from infrastructure import cookie_auth

router = fastapi.APIRouter()


@router.get('/blog')
@template(template_file='blog/index.pt')
async def index(request: Request):
    vm = BlogViewModel(request)
    await vm.load()
    return vm.to_dict()


@router.get('/blog/create')
@template(template_file='blog/create.pt')
async def create_post(request: Request):
    if not cookie_auth.get_user_id_via_auth_cookie(request):
        return RedirectResponse(url='/account/login', status_code=status.HTTP_302_FOUND)
    
    vm = PostViewModel(request)
    return vm.to_dict()


@router.post('/blog/create')
@template(template_file='blog/create.pt')
async def create_post(request: Request):
    if not cookie_auth.get_user_id_via_auth_cookie(request):
        return RedirectResponse(url='/account/login', status_code=status.HTTP_302_FOUND)
    
    vm = PostViewModel(request)
    await vm.load()
    
    if vm.error:
        return vm.to_dict()
    
    # Create new post
    post = Post(
        title=vm.title,
        content=vm.content,
        author_id=cookie_auth.get_user_id_via_auth_cookie(request),
        status='draft'
    )
    
    session = db_session.create_session()
    session.add(post)
    session.commit()
    
    return RedirectResponse(url=f'/blog/{post.id}', status_code=status.HTTP_302_FOUND)


@router.get('/blog/{post_id}')
@template(template_file='blog/post.pt')
async def post(request: Request, post_id: int):
    vm = PostViewModel(request)
    await vm.load(post_id)
    return vm.to_dict() 