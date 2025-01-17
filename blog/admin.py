from django.contrib import admin
from blog.models import Category, Post
from markdownx.admin import MarkdownxModelAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.db.models import Count


# These classes are for customizing the appearance of models in the admin panel.
# Accepts lists or tuples. I use a list for a tuple of one object.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Model overview management page.
    list_display = ("name", "post_count", "view_category")
    ordering = ["name"]
    list_per_page = 20

    # When adding or editing a category.
    readonly_fields = ["get_posts", "view_category"]


    # Gets the number of posts in a category and make this column sortable.
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(post_count=Count("posts"))

    @admin.display(description="number of posts")
    def post_count(self, obj):
        return obj.post_count

    post_count.admin_order_field = "post_count"
    

    # Generates a list of links to posts under a category.
    # 'posts' in posts.all() is the related_name of the model Post.categories.
    @admin.display(description="posts")
    def get_posts(self, obj):
        return self.links_to_posts(obj.posts.all().order_by("-created_on"))
    
    @classmethod
    def links_to_posts(cls, objects_list):
        posts_list = '<ol class="category_posts_list">'

        for post in objects_list:
            link = reverse('admin:%s_%s_change'%(post._meta.app_label, post._meta.model_name), args=[post.id])
            posts_list += '<li><a href="%s">%s</a></li>'%(link, post.title)
        
        posts_list += '</ol>'
        return format_html(posts_list)
    

    # Link to the category from the admin page.
    def view_category(self, obj):
        link_url = reverse("blog_category", kwargs={"category": obj.name})
        link = '<a href="%s" target="_blank">view</a>'%(link_url)
        return format_html(link)

    # Resolves the error message when creating a new category,
    # because there is no link to the category yet.
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["get_posts", "view_category"]
        else:
            return ["get_posts"]



@admin.register(Post)
class PostAdmin(MarkdownxModelAdmin):
    # Model overview management page.
    list_display = ("title", "created_on", "last_modified", "view_post")
    ordering = ["-created_on"]
    list_per_page = 20
    actions_on_top = False
    actions_on_bottom = True
    search_fields = ["title"]
    list_filter = ("created_on", "last_modified")

    # When adding or editing a post.
    readonly_fields = ["view_post"]
    filter_horizontal = ["categories"]


    # Resizes the title's text box.
    def get_form(self, request, obj=None, **kwargs):
        form = super(PostAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields["title"].widget.attrs["style"] = "width: 45em;"
        return form

    # Link to the published post.
    def view_post(self, obj):
        link_url = reverse("blog_detail", kwargs={"pk": obj.id})
        link = '<a href="%s" target="_blank">view</a>'%(link_url)
        return format_html(link)

    # Resolves the error message when creating a new post,
    # because there is no link to the published post yet.
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["view_post"]
        else:
            return []

