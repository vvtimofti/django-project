from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_posts_from_page(post_list, page):
    paginator = Paginator(post_list, 5)
    try:
        posts = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        posts = paginator.page(1)

    return posts