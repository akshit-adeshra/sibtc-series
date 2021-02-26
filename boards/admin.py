from django.contrib import admin
from django.utils.html import format_html
from django.utils.http import urlencode

from .models import *


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'view_topics_link')

    def view_topics_link(self, obj):
        count = Topic.objects.filter(board__name=obj).count()
        url = (
                reverse("admin:boards_topic_changelist")
                + "?"
                + urlencode({"board__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Topics</a>', url, count)

    view_topics_link.short_description = "Topics"


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('subject', 'board', 'last_updated', 'starter', 'view_posts_link')
    readonly_fields = ['last_updated', ]

    def view_posts_link(self, obj):
        count = Post.objects.filter(topic__subject=obj).count()
        url = (
                reverse("admin:boards_post_changelist")
                + "?"
                + urlencode({"topic__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Posts</a>', url, count)

    view_posts_link.short_description = "Posts"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('message', 'topic', 'created_at', 'created_by', 'updated_by')
    readonly_fields = ['created_at', ]

    # custom func to make the topic field clickable
    # def view_associated_topic(self, obj):
    #     url = (
    #         reverse("admin:boards_topic_changelist")
    #         + "?"
    #         + urlencode({"topic__subject": f"{obj.id}"})
    #     )
    #     return format_html('<a href="{}">It\'s Topic</a>', url)
    #
    # view_associated_topic.short_description = 'Topic'
