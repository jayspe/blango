import logging
from django.shortcuts import render, get_object_or_404

from django.utils import timezone
from blog.models import Post
#from django.shortcuts import render

from django.shortcuts import redirect
from blog.forms import CommentForm

from django.urls import reverse

logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    #posts = Post.objects.filter(published_at__lte=timezone.now())
    posts = Post.objects.filter(published_at__lte=timezone.now()).select_related("author") 
    ## with only method
    # posts = (
    #     Post.objects.filter(published_at__lte=timezone.now())
    #     .select_related("author")
    #     .only("title", "summary", "content", "author", "published_at", "slug")
    # )
    ## with defer method
    # posts = (
    #     Post.objects.filter(published_at__lte=timezone.now())
    #     .select_related("author")
    #     .defer("created_at", "modified_at", "published_at")
    # )

    logger.debug("Got %d posts", len(posts))
    return render(request, "blog/index.html", {"posts": posts})
    

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_active:
        if request.method == "POST":
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.content_object = post
                comment.creator = request.user
                comment.save()
                return redirect(request.path_info)
        else:
            comment_form = CommentForm()
    else:
        comment_form = None
    #return render(request, "blog/post-detail.html", {"post": post})
    return render(
        request,
        "blog/post-detail.html", 
        {"post": post, "comment_form": comment_form}, 
        logger.info("Created comment on Post %d for user %s", post.pk, request.user)
    )

def get_ip(request):
  """ view to return the IP address that’s connected to Django"""
  from django.http import HttpResponse
  return HttpResponse(request.META['REMOTE_ADDR'])

def post_table(request):
    return render(
        request, "blog/post-table.html", {"post_list_url": reverse("post-list")}
    )