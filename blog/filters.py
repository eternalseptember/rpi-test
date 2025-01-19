from blog.models import Post, Category
import django_filters


class PostFilter(django_filters.FilterSet):

    class Meta:
        model = Post
        fields = {
            "title": ['icontains'],
            "body": ['icontains'],
            "created_on": ['date', 'date__gte', 'date__lte'],
            #"categories": ['exact']
            }

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters["created_on__date"].label="Created on"
        self.filters["created_on__date__gte"].label="Created after"
        self.filters["created_on__date__lte"].label="Created before"


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
