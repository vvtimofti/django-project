from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.db.models import F

from apps.posts.forms import PostForm
from apps.posts.models import Post, Repost
from apps.accounts.models import Profile
from utils.utils import get_posts_from_page


@login_required
def post_detail(request, username, post_key):
    post = get_object_or_404(
        Post.objects.select_related(
            "parent_post", "parent_post__user"),
        user__username=username,
        post_key=post_key
    )
    current_url = request.htmx.current_url_abs_path or post.get_absolute_url()

    if current_url != post.get_absolute_url():
        post.views_count += 1
        post.save()

    parent_posts = []
    current_post = post
    while current_post.parent_post:
        parent_posts.insert(0, current_post.parent_post)
        current_post = current_post.parent_post

    comments = get_posts_from_page(
        post.replies.all(), request.GET.get('page', 1))

    context = {
        'page_title': 'Post Detail',
        'post': post,
        'posts': comments,
        'parent_posts': parent_posts,
        'first_page': request.GET.get('page', 1) == 1
    }
    return render(request, 'posts/post_detail.html', context)


def post_create(request, username=None, post_key=None):
    parent_post = None
    is_reply = False

    if post_key:
        parent_post = get_object_or_404(Post, user__username=username, post_key=post_key)
        is_reply = True

    form = PostForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            is_video = False
            if request.FILES:
                is_video = request.FILES["media"].content_type.startswith("video")
            post = form.save(commit=False)
            post.user = request.user
            post.parent_post = parent_post
            post.is_reply = is_reply
            post.is_video = is_video
            post.save()

            messages.success(request, 'Post created successfully')

    if is_reply:
        return redirect(parent_post.get_absolute_url())
    return redirect("home")


@login_required
def post_delete(request, username, post_key):
    post = get_object_or_404(Post, user__username=username, post_key=post_key)

    if request.user == post.user or request.user.is_staff:
        post.delete()
        messages.success(request, "Post deleted successfully")
        if post.parent_post:
            return redirect(post.parent_post.get_absolute_url())
        else:
            return redirect("home")
    else:
        return render(request, "core/error_page.html", {"message": "Unauthorized deletion"})


@login_required
def like_post(request, username, post_key):
    post = get_object_or_404(Post, user__username=username, post_key=post_key)
    context = {"post": post}

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return render(request, "posts/partials/like_section.html", context)


@login_required
def toggle_repost(request, username, post_key):
    post = get_object_or_404(Post, user__username=username, post_key=post_key)
    repost, created = Repost.objects.get_or_create(
        user=request.user, post=post)
    context = {"post": post}

    if not created:
        repost.delete()

    return render(request, "posts/partials/repost_section.html", context)


@login_required
def toggle_bookmark(request, username, post_key):
    post = get_object_or_404(Post, user__username=username, post_key=post_key)
    context = {"post": post}

    if request.user in post.bookmarks.all():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)

    return render(request, "posts/partials/bookmark_section.html", context)


@login_required
def search_view(request):
    search_text = request.POST.get("search")
    results = Profile.objects.filter(user__username__icontains=search_text).exclude(
        user=request.user) if search_text else None
    context = {"results": results}
    return render(request, 'core/includes/search-results.html', context)
