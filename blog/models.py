from django.db import models
from django.utils.timezone import now
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="category name")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    created_on = models.DateTimeField(default=now)
    last_modified = models.DateTimeField(auto_now=True)
    body = MarkdownxField()
    categories = models.ManyToManyField("Category", related_name="posts")

    # Create a property that returns the markdown instead
    @property
    def formatted_markdown(self):
        return markdownify(self.body)

    def __str__(self):
        return self.title

