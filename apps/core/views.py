from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from itertools import chain
from django.urls import reverse_lazy
from django.db.models import Count

from apps.accounts import forms
from apps.accounts.models import Profile
from apps.posts.models import Post, Repost, Notification
from utils.utils import get_posts_from_page


User = get_user_model()


def index(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "_base.html", {"page_title": "join"})


@login_required
def home_view(request):
    post_list = Post.objects.filter(is_reply=False)
    posts = get_posts_from_page(post_list, request.GET.get('page', 1))

    context = {
        "page_title": "home",
        "first_page": request.GET.get('page', 1) == 1,
        "posts": posts,
    }

    return render(request, "core/home.html", context)


@login_required
def following_view(request):
    following_users = request.user.profile.following.select_related("profile")
    following_posts = Post.objects.filter(
        user__profile__in=following_users, is_reply=False).select_related('user__profile')
    following_reposts = Repost.objects.filter(
        user__profile__in=following_users).select_related('post', 'user__profile')

    combined_qs = sorted(
        chain(following_posts, following_reposts),
        key=lambda obj: obj.datetime,
        reverse=True
    )

    for index, post in enumerate(combined_qs):
        if isinstance(post, Repost):
            post.post.repost_user = post.user
            combined_qs[index] = post.post

    posts = get_posts_from_page(combined_qs, request.GET.get('page', 1))

    context = {
        "page_title": "home",
        "visible": True,
        "posts": posts,
        "first_page": request.GET.get('page', 1) == 1
    }
    return render(request, "core/following.html", context)


@login_required
def profile_view(request, username):
    user = User.objects.prefetch_related("user_posts").get(username=username)
    post_list = user.user_posts.filter(is_reply=False)
    reposts = Repost.objects.filter(user=user)

    combined_qs = sorted(
        chain(post_list, reposts),
        key=lambda obj: obj.datetime,
        reverse=True
    )

    for index, post in enumerate(combined_qs):
        if isinstance(post, Repost):
            post.post.repost_user = post.user
            combined_qs[index] = post.post

    posts = get_posts_from_page(combined_qs, request.GET.get('page', 1))

    context = {
        "page_title": username,
        "user": user,
        "posts": posts,
        "first_page": request.GET.get('page', 1) == 1
    }
    return render(request, "core/profile.html", context)


@login_required
def profile_replies_view(request, username):
    page = request.GET.get('page', 1)
    first_page = page == 1

    user = User.objects.prefetch_related("user_posts").get(username=username)
    post_list = user.user_posts.filter(is_reply=True)

    posts = get_posts_from_page(post_list, page)

    context = {
        "page_title": f"{username} Replies",
        "posts": posts,
        "user": user,
        "first_page": first_page
    }
    return render(request, "core/profile_replies.html", context)


@login_required
def profile_likes_view(request, username):
    page = request.GET.get('page', 1)
    first_page = page == 1

    user = User.objects.prefetch_related("u_likes").get(username=username)
    post_list = list(user.u_likes.all())

    for index, like_object in enumerate(post_list):
        post_list[index] = like_object.post

    posts = get_posts_from_page(post_list, page)

    context = {
        "page_title": f"{username} Likes",
        "posts": posts,
        "user": user,
        "first_page": first_page
    }
    return render(request, "core/profile_likes.html", context)


@login_required
def profile_settings_view(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_settings', username=request.user.username)
    else:
        form = forms.ProfileForm(instance=profile)

    if request.user != user:
        return render(request, "core/error_page.html", {"message": "You don't have access to this page"})

    context = {
        "page_title": f"{username} Settings",
        "form": form,
        "first_page": True
    }

    return render(request, "core/profile_settings.html", context)


@login_required
def bookmarks_view(request):
    page = request.GET.get('page', 1)
    first_page = page == 1

    bookmarks = list(request.user.u_bookmarks.all())

    for index, bookmark_object in enumerate(bookmarks):
        bookmarks[index] = bookmark_object.post

    posts = get_posts_from_page(bookmarks, page)

    context = {
        "page_title": "bookmarks",
        "posts": posts,
        "first_page": first_page
    }
    return render(request, "core/bookmarks.html", context)


@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(
        receiver=request.user).order_by("-timestamp")

    if request.method == "POST":
        Notification.objects.filter(id=request.POST["id"]).update(is_read=True)
        return HttpResponse("")

    if request.method == "DELETE":
        notifications.delete()

    context = {
        "page_title": "notifications",
        "notifications": notifications,
    }

    return render(request, "core/notifications.html", context)


@login_required
def get_unread_notifications(request):
    notifications = Notification.objects.filter(
        receiver=request.user, is_read=False).order_by("-timestamp")
    return render(request, 'core/includes/new_notification.html', {"notifications": notifications})


@login_required
def messages_view(request):
    chatrooms = request.user.chat_rooms.annotate(
        message_count=Count('chat_messages')
    ).filter(message_count__gte=1)

    chat_partners = User.objects.exclude(
        id=request.user.id).filter(chat_rooms__in=chatrooms)

    context = {
        "page_title": "messages",
        "chatrooms": chatrooms,
        "members": chat_partners,
    }
    return render(request, "core/messages.html", context)


@login_required
def change_theme(request):
    if request.method == 'POST':
        theme = request.POST["theme-dropdown"]
        request.session['theme'] = theme
        return HttpResponse(status=200)
    return HttpResponse(status=400)
