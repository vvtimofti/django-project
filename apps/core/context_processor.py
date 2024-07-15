from django.urls import resolve
from apps.posts.forms import PostForm
from apps.posts.models import Notification


def navbar_processor(request):
    if request.user.is_authenticated:
        context = {
            "tabs": [
                {
                    "name": "home",
                    "icon": "home",
                },
                {
                    "name": "notifications",
                    "icon": "bell",
                },
                {
                    "name": "messages",
                    "icon": "message",
                },
                {
                    "name": "bookmarks",
                    "icon": "bookmark",
                },
            ]
        }

        context["page_title"] = resolve(request.path_info).url_name
        context["user"] = request.user
        context["post_form"] = PostForm
        context["notifications"] = Notification.objects.filter(receiver=request.user, is_read=False).exists()
    
        return context
    return {}


def htmx_processor(request):
    first_page = request.GET.get('page', 1) == 1

    if not first_page:
        base_template = "_empty.html"
    elif request.htmx:
        base_template = "_partial.html"
    else:
        base_template = "_base.html"

    return {"base_template": base_template}

