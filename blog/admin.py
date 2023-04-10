from django.contrib import admin
from blog.models import Tag, Post

# class PostAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("title",)}

# Changed PostAdmin to show slug and published_at in the Post list
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('slug', 'published_at')

# Register your models here.
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
