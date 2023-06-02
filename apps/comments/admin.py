from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from apps.comments.models import Comment, CommentRating

admin.site.register(Comment, MPTTModelAdmin)
admin.site.register(CommentRating)
