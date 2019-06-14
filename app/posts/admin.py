from __future__ import unicode_literals

import django.contrib.auth.admin
import django.contrib.auth.models
from django.contrib import admin, auth
from app.posts.models import Post, PostVisibility


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'visibility', 'owner')
    list_filter = ('owner', 'visibility')
    search_fields = ('owner', 'visibility')
    raw_id_fields = ('owner', )


class VisibilityAdmin(admin.ModelAdmin):
    raw_id_fields = ('post', 'user')

admin.site.register(Post, PostAdmin)
admin.site.register(PostVisibility, VisibilityAdmin)
