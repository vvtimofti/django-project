from django.contrib import admin
from apps.posts.models import Post, Repost, Notification


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['user', 'post_key', 'datetime', 'is_reply', 'get_likes_count']
    search_fields = ['user__username', 'post_content', 'post_key'] 
    list_filter = ['datetime', 'is_reply']

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    get_likes_count.short_description = 'Likes'
    

admin.site.register(Repost)
admin.site.register(Notification)
