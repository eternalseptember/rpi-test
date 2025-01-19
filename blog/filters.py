from blog.models import Post, Category
import django_filters
from django_filters import ModelChoiceFilter


class PostFilter(django_filters.FilterSet):
    # The following makes the categories menu a single-selection dropdown box
    # with the empty label as the empty choice. 
    # Current label is the same thing as the default label, 
    # but doing it this way to be an explicit reference later.
    # An equivalent statement can be set in the __init__ override.
    # categories = ModelChoiceFilter(queryset=Category.objects.all().order_by("name"), empty_label="---------")

    class Meta:
        model = Post
        fields = {
            "title": ['icontains'],
            "body": ['icontains'],
            "created_on": ['date', 'date__gte', 'date__lte'],
            "categories": ['exact']
            }

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters["created_on__date"].label="Created on"
        self.filters["created_on__date__gte"].label="Created on or after"
        self.filters["created_on__date__lte"].label="Created on or before"

        self.filters["categories"].queryset=Category.objects.all().order_by("name")
        


    # This override so that the queryset returns *NOTHING* 
    # instead of *EVERYTHING* if there's an invalid filter.
    @property
    def qs(self):
        if not hasattr(self, '_qs'):
            qs = self.queryset.all()
            if self.is_bound:
                if self.form.is_valid():
                    qs = self.filter_queryset(qs)
                else:
                    qs = self.queryset.none()
            self._qs = qs
        return self._qs
