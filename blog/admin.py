from django.contrib import admin
from blog.models import Category, Post
from markdownx.admin import MarkdownxModelAdmin
from django.urls import reverse
from django.utils.html import format_html


# These classes are for customizing the appearance of models in the admin panel.
# Accepts lists or tuples. I use a list for a tuple of one object.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_display = ('name', 'get_num_posts')
    readonly_fields = ['get_posts']

    @admin.display(description="number of posts")
    def get_num_posts(self, obj):
        return len(obj.posts.all())

    @admin.display(description='posts')
    def get_posts(self, obj):
        return self.links_to_posts(obj.posts.all().order_by("-created_on"))
    
    @classmethod
    def links_to_posts(cls, objects_list):
        posts_list = '<ol class="category_posts_list">'
        num_of_posts = len(objects_list)

        for i in range(num_of_posts):
            post = objects_list[i]
            link = reverse('admin:%s_%s_change'%(post._meta.app_label, post._meta.model_name), args=[post.id])
            posts_list += '<li><a href="%s">%s</a>'%(link, post.title)

            if (i+1) < num_of_posts:
                posts_list += '<br>'
        
        posts_list += '</ol>'
        return format_html(posts_list)



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

