from blog.models import Post
import django_filters

#from django.db import models
#from django_filters import DateFilter


class PostFilter(django_filters.FilterSet):

    class Meta:
        model = Post
        fields = {
            "title": ['icontains'],
            "body": ['icontains'],
            "created_on": ['exact', 'gte', 'lte'],
            "categories": []
            }

        """
        filter_overrides = {
            models.DateTimeField: {
                'filter_class': django_filters.DateFilter
            }
        }
        """
