from django import template

register = template.Library()

from boards.models import *


@register.simple_tag
def total_count(var):
    if var == 'Board':
        var = Board.objects.count()
    if var == 'Topic':
        var = Topic.objects.count()
    if var == 'Post':
        var = Post.objects.count()
    return var

# @register.simple_tag()
# def total_topics():
#     return Topic.objects.count()
#
#
# @register.simple_tag()
# def total_posts():
#     return Post.objects.count()
