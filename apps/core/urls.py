from django.urls import path, include

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home_view, name="home"),
    path("home/following/", views.following_view, name="following"),
    path("messages/", views.messages_view, name="messages"),
    path("bookmarks/", views.bookmarks_view, name="bookmarks"),
    path("@<str:username>/posts/", views.profile_view, name="profile"),
    path("@<str:username>/replies/", views.profile_replies_view, name="profile_replies"),
    path("@<str:username>/likes/", views.profile_likes_view, name="profile_likes"),
    path("@<str:username>/settings/", views.profile_settings_view, name="profile_settings"),
    path("notifications/", views.notifications_view, name="notifications"),
    path("notifications/fetch", views.get_unread_notifications, name="fetch_notifications"),
    path("change-theme/", views.change_theme, name="change_theme"),
]