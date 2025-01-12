from django.contrib import admin
from blog.models import Category, Post
from markdownx.admin import MarkdownxModelAdmin


# These classes are for customizing the appearance of models in the admin panel.
# Accepts lists or tuples. I use a list for a tuple of one object.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ['name']


@admin.register(Post)
class PostAdmin(MarkdownxModelAdmin):
    actions_on_top = False
    actions_on_bottom = True
    list_display = ('title', 'created_on', 'last_modified')
    ordering = ['-created_on']
    search_fields = ['title']
    list_filter = ('created_on', 'last_modified')
    filter_horizontal = ['categories']

    def get_form(self, request, obj=None, **kwargs):
        form = super(PostAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['title'].widget.attrs['style'] = 'width: 45em;'
        return form

    

