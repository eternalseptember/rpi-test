from blog.calendar import BlogHTMLCalendar
from blog.filters import PostFilter
from blog.models import Post, Category
from datetime import date
from django.contrib.postgres.search import SearchVector, SearchQuery
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView



paginate_count = 5  # This is basically a global variable.
def paginate(queryset, request):
    paginator = Paginator(queryset, paginate_count)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)



def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")

    # Output to Template
    context = {
        "page_obj": paginate(posts, request),
    }
    return render(request, "blog/index.html", context)



def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name = category
        ).order_by("-created_on")

    # Output to Template
    category = Category.objects.get(name=category)
    category_edit_url = reverse("admin:{}_{}_change"
                  .format(category._meta.app_label, category._meta.model_name), 
                  args=[category.id])
    page_title = 'category: <a href="{}">{}</a>'.format(category_edit_url, category)

    context = {
        "site_title": 'Category: {}'.format(category),
        "page_title": page_title,
        "description": category.description,
        "page_obj": paginate(posts, request),
    }
    return render(request, "blog/category.html", context)



def blog_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)

        # Output to Template
        post_edit_url = reverse("admin:{}_{}_change"
                  .format(post._meta.app_label, post._meta.model_name), 
                  args=[post.pk])

        context = {
            "site_title": post.title,
            "page_title": '<a href="{}">{}</a>'.format(post_edit_url, post.title),
            "post": post,
        }
        return render(request, "blog/detail.html", context)

    except Post.DoesNotExist:
        return render(None, "blog/404.html", context={})



def blog_search(request):
    query = request.GET.get("q")

    if query:
        # Basic search with postgres
        search_results = Post.objects.annotate(
            search=SearchVector("title", "body")
            ).filter(search=SearchQuery(query))

    else:
        search_results = Post.objects.none()

    # Output to Template
    context = {
        "site_title": 'Search: {}'.format(query),
        "page_title": 'search: {}'.format(query),
        "page_obj": paginate(search_results, request),
        "query": query,
    }
    return render(request, "blog/search_results.html", context)



def advanced_search(request):
    queryset = Post.objects.all()
    selected_categories = request.GET.getlist("categories")  # This is getlist instead of regular get!
    post_filter = PostFilter(request.GET, selected_categories=selected_categories, queryset=queryset)

    """
    THIS SECTION NEEDS CAREFUL ATTENTION!
    FIX THE FIELD NAMES AFTER MODIFYING FILTERS!

    This section makes the advanced search page show *NOTHING* instead
    of *EVERYTHING* if there are no filters applied.

    This combined with the qs override in the filter (filters.py) makes
    the advanced search page show no posts when first loading into the
    page and when there's an invalid filter applied.
    """
    s1 = request.GET.get("title__icontains")  # used for highlighting
    s2 = request.GET.get("body__icontains")  # used for highlighting
    s3 = request.GET.get("created_on__date")
    s4 = request.GET.get("created_on__date__gte")
    s5 = request.GET.get("created_on__date__lte")
    s6 = selected_categories  # being passed to PostFilter object for filtering
    s7 = request.GET.get("anniversary_date")

    # Omitting a check for the custom filters ("and_categories" and "sort_how").
    # If those are the only options selected, then return nothing.
    if s1 or s2 or s3 or s4 or s5 or s6 or s7:
        search_results = post_filter.qs
    else:
        search_results = Post.objects.none()


    # Output to Template
    # Get category names from ID to make highlighting easier.
    query_categories = [Category.objects.get(id=category_id).name for category_id in s6]

    context = {
        "site_title": 'Advanced Search',
        "form": post_filter.form,
        "page_obj": paginate(search_results, request),
        "query_title": s1,  # for highlighting
        "query_body": s2,  # for highlighting
        "query_categories": query_categories,  # for highlighting
    }
    return render(request, "blog/advanced_search.html", context)



class ArchiveTimeView(TemplateView):
    """
    The master view that the daily, monthly, and yearly archives inherit from.
    """
    def get_prev_and_next(self, **kwargs):
        """
        prev_link, this_link, next_link are lists in the order of [year, month, day].
        Returns a list of [prev_link, this_link, next_link].
        """	
        this_link = list(kwargs.values())
        this_index = self.dates_list.index(this_link)

        # Previous (unit of time), skipping over empty (unit of time).
        prev_index = this_index - 1
        prev_link = self.dates_list[prev_index] if self.is_valid_index(prev_index) else None

        # Next (unit of time), skipping over empty (unit of time).
        next_index = this_index + 1
        next_link = self.dates_list[next_index] if self.is_valid_index(next_index) else None

        return [prev_link, this_link, next_link]

    def is_valid_index(self, index):
        return (0 <= index) and (index < len(self.dates_list))



class ArchiveDayView(ArchiveTimeView):
    template_name = "blog/archive_day.html"

    def get_context_data(self, **kwargs):
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]
        day_date = date(year, month, day)

        search_results = Post.objects.filter(
            created_on__date = day_date
            ).order_by("-created_on")

        # Steps for nav links
        dates = Post.objects.dates("created_on", "day", "ASC")
        self.dates_list = [[date.year, date.month, date.day] for date in dates]
        nav_links = self.get_prev_and_next(**kwargs)

        # Output to Template
        day_date = day_date.strftime("%b %-d, %Y")

        context = {
            "site_title": day_date,
            "page_title": day_date,
            "page_obj": search_results,
            "prev_day": nav_links[0],
            "this_day": nav_links[1],
            "next_day": nav_links[2],
        }
        return context



class ArchiveMonthView(ArchiveTimeView):
    template_name = "blog/archive_month.html"

    def get_context_data(self, **kwargs):
        year = self.kwargs["year"]
        month = self.kwargs["month"]

        search_results = Post.objects.filter(
            created_on__year = year,
            created_on__month = month
            ).order_by("-created_on")

        # Steps for nav links
        dates = Post.objects.dates("created_on", "month", "ASC")
        self.dates_list = [[date.year, date.month] for date in dates]
        nav_links = self.get_prev_and_next(**kwargs)

        # Output to Template
        month_date = date(year, month, 1).strftime("%B %Y")

        context = {
            "site_title": month_date,
            "page_title": month_date,
            "page_obj": search_results,
            "prev_month": nav_links[0],
            "this_month": nav_links[1],
            "next_month": nav_links[2],
        }
        return context



class ArchiveYearView(ArchiveTimeView):
    template_name = "blog/archive_year.html"

    def get_context_data(self, **kwargs):
        year = self.kwargs["year"]

        posts_list = Post.objects.filter(
            created_on__year = year
            ).order_by("created_on")

        search_results = posts_list.annotate(month=TruncMonth("created_on"))
        cal = BlogHTMLCalendar(year, posts_list).printyear()

        # Steps for nav links
        dates = Post.objects.dates("created_on", "year", "ASC")
        self.dates_list = [[date.year] for date in dates]
        nav_links = self.get_prev_and_next(**kwargs)

        # Output to Template
        context = {
            "site_title": 'Year {}'.format(year),
            "page_obj": search_results,
            "prev_year": nav_links[0],
            "this_year": nav_links[1],
            "next_year": nav_links[2],
            "cal": cal,
        }
        return context



class ArchiveView(TemplateView):
    template_name = "blog/archive.html"

    def get_context_data(self, **kwargs):
        dates = Post.objects.dates("created_on", "year", "DESC")
        years = [date.year for date in dates]

        # Output to Template
        context = {
            "site_title": 'Archives',
            "page_title": 'Archives',
            "years": years,
        }
        return context



