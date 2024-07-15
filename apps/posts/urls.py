from django.urls import path

from . import views


urlpatterns = [
    path("create/", views.post_create, name="post_create"),
    path("<str:username>/<uuid:post_key>/", views.post_detail, name="post_detail"),
    path("<str:username>/<uuid:post_key>/create/", views.post_create, name="post_create"),
    path("<str:username>/<uuid:post_key>/delete/", views.post_delete, name="post_delete"),
    path("<str:username>/<uuid:post_key>/like/", views.like_post, name="like_post"),
    path("<str:username>/<uuid:post_key>/bookmark/", views.toggle_bookmark, name="toggle_bookmark"),
    path("<str:username>/<uuid:post_key>/repost/", views.toggle_repost, name="toggle_repost"),
]

htmx_urlpatterns = [
    path("search/", views.search_view, name="search"),
]

urlpatterns += htmx_urlpatterns