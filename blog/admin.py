from django.contrib import admin
from .models import Post, Comment, Tag
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'approved')
    list_filter = ('approved',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Tag)


from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'approved')
    list_filter = ('approved',)
    actions = ['approve_posts']

    def approve_posts(self, request, queryset):
        queryset.update(approved=True)
    approve_posts.short_description = "Mark selected posts as approved"



