from django import template

from blog.models import Comment

register = template.Library()


@register.inclusion_tag('blog/includes/latest_comments.html')
def show_latest_comments(count=5):
    comments = Comment.objects.select_related('author').filter(status='published').order_by('-time_create')[:count]
    return {'comments': comments}
