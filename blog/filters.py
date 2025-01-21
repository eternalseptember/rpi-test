from blog.models import Post, Category
from django.forms import CheckboxInput
import django_filters
from django_filters import BooleanFilter, ChoiceFilter, ModelMultipleChoiceFilter


class PostFilter(django_filters.FilterSet):
    """
    This is the Advanced Search form.
    """
    date_sort_choices=[
        ('desc', ('Desc (newest first)')),
        ('asc', ('Asc (oldest first)'))
        ]

    # Custom non-model fields
    categories = ModelMultipleChoiceFilter(
        queryset=Category.objects.all().order_by("name"), 
        field_name="categories",
        lookup_expr="exact",
        )
    and_categories = BooleanFilter(label="Categories AND?", widget=CheckboxInput, method="and_search")
    sort_how = ChoiceFilter(choices=date_sort_choices, label="Sort by date?", empty_label="----", method="sort_by_date")


    class Meta:
        model = Post
        fields = {
            "title": ["icontains"],
            "body": ["icontains"],
            "created_on": ["date", "date__gte", "date__lte"],
            }


    def __init__(self, *args, **kwargs):
        self.selected_categories = kwargs.pop('selected_categories')
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters["created_on__date"].label="Created on"
        self.filters["created_on__date__gte"].label="Created on or after"
        self.filters["created_on__date__lte"].label="Created on or before"


    def and_search(self, queryset, field_name, value):
        """
        "field_name" is "and_categories".
        "value" is boolean True or False.
        If False, then return the normal search results (which is done with boolean 'OR').
        If True, then run boolean 'AND' on the queryset with all of the selected categories 
        (which are passed as categories__id).
        """
        if value is False:
            return queryset
        for selected_category in self.selected_categories:
            queryset = queryset.filter(categories__id = selected_category)
        return queryset


    def sort_by_date(self, queryset, field_name, value):
        """
        "field_name" is "sort_how".
        "value" could be "desc", "asc", or the empty choice, presumbly None,
        which sorts by post.id by default.
        """
        if value == "desc":
            return queryset.order_by("-created_on")
        elif value == "asc":
            return queryset.order_by("created_on")
        return queryset


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
