from blog.calendar import BlogHTMLCalendar
from blog.filters import PostFilter
from blog.models import Post, Category
from datetime import date
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import TruncMonth
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView


def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Output to Template
    context = {
        "page_obj": page_obj
    }
    return render(request, "blog/index.html", context)



def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name = category
        ).order_by("-created_on")

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Output to Template
    category = Category.objects.get(name=category)
    category_edit_url = reverse("admin:{}_{}_change"
                  .format(category._meta.app_label, category._meta.model_name), 
                  args=[category.id])
    page_title = '<h2>category: <a href="{}">{}</a></h2>'.format(category_edit_url, category)
    page_title += '<span class="category_description">{}</span>'.format(category.description)

    context = {
        "site_title": '| Category: {}'.format(category),
        "page_title": page_title,
        "page_obj": page_obj,
    }
    return render(request, "blog/index.html", context)



def blog_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)

        # Output to Template
        post_edit_url = reverse("admin:{}_{}_change"
                  .format(post._meta.app_label, post._meta.model_name), 
                  args=[post.pk])

        context = {
            "site_title": '| {}'.format(post.title),
            "page_title": '<h2><a href="{}">{}</a></h2>'.format(post_edit_url, post.title),
            "post": post,
        }
        return render(request, "blog/detail.html", context)

    except Post.DoesNotExist:
        return render(None, "blog/404.html", context={})



def blog_search(request):
    query = request.GET.get("q")
    if query:
        search_results = Post.objects.filter(
            Q(title__icontains = query) |
            Q(body__icontains = query)
            ).distinct().order_by("-created_on")

    else:
        search_results = Post.objects.none()

    paginator = Paginator(search_results, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Output to Template
    context = {
        "site_title": '| Search: {}'.format(query),
        "page_title": '<h2>search: {}</h2>'.format(query),
        "page_obj": page_obj,
        "query": query
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
    s7 = request.GET.get("and_categories")  # non-model field

    # Omitting a check for s7 because if only the AND button is selected, then return nothing.
    if s1 or s2 or s3 or s4 or s5 or s6:
        search_results = post_filter.qs
    else:
        search_results = Post.objects.none()


    paginator = Paginator(search_results, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)	

    # Output to Template
    context = {
        "site_title": '| Advanced Search',
        "page_title": '<h2>Advanced Search</h2>',
        "form": post_filter.form,
        "page_obj": page_obj,
        "query_title": s1,  # for highlighting
        "query_body": s2,  # for highlighting
    }
    return render(request, "blog/advanced_search.html", context)



class ArchiveDayView(TemplateView):
    template_name = "blog/archive_day.html"

    def get_context_data(self, **kwargs):
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]
        day_date = date(year, month, day)

        search_results = Post.objects.filter(
            created_on__date = day_date
            ).order_by("-created_on")

        # Output to Template
        prev_link, this_link, next_link = self.get_prev_and_next(year, month, day)

        context = {
            "site_title": '| {}'.format(day_date.strftime("%b %-d, %Y")),
            "page_title": '<h2>{}</h2>'.format(day_date.strftime("%b %-d, %Y")),
            "page_obj": search_results,
            "prev_day": prev_link,
            "this_day": this_link,
            "next_day": next_link
        }
        return context

    def get_prev_and_next(self, year, month, day):
        """
        prev_link, this_link, next_link are lists in the order of [year, month, day].
        """
        # This section slightly differs depending on type of archive.
        dates = Post.objects.dates("created_on", "day", "ASC")
        self.dates_list = [[date.year, date.month, date.day] for date in dates]
        this_link = [year, month, day]

        # The rest of this section is the same.	
        this_index = self.dates_list.index(this_link)

        # Previous (unit of time), skipping over empty (unit of time).
        prev_index = this_index - 1
        prev_link = self.dates_list[prev_index] if self.is_valid_index(prev_index) else None

        # Next (unit of time), skipping over empty (unit of time).
        next_index = this_index + 1
        next_link = self.dates_list[next_index] if self.is_valid_index(next_index) else None

        return prev_link, this_link, next_link

    def is_valid_index(self, index):
        return (0 <= index) and (index < len(self.dates_list))



class ArchiveMonthView(TemplateView):
    template_name = "blog/archive_month.html"

    def get_context_data(self, **kwargs):
        year = self.kwargs["year"]
        month = self.kwargs["month"]

        search_results = Post.objects.filter(
            created_on__year = year,
            created_on__month = month
            ).order_by("-created_on")

        # Output to Template
        month_date = date(year, month, 1)
        prev_link, this_link, next_link = self.get_prev_and_next(year, month)

        context = {
            "site_title": '| {}'.format(month_date.strftime("%B %Y")),
            "page_title": '<h2>{}</h2>'.format(month_date.strftime("%B %Y")),
            "page_obj": search_results,
            "prev_month": prev_link,
            "this_month": this_link,
            "next_month": next_link
        }
        return context

    def get_prev_and_next(self, year, month):
        """
        prev_link, this_link, next_link are lists in the order of [year, month].
        """
        # This section slightly differs depending on type of archive.
        dates = Post.objects.dates("created_on", "month", "ASC")
        self.dates_list = [[date.year, date.month] for date in dates]
        this_link = [year, month]

        # The rest of this section is the same.
        this_index = self.dates_list.index(this_link)

        # Previous (unit of time), skipping over empty (unit of time).
        prev_index = this_index - 1
        prev_link = self.dates_list[prev_index] if self.is_valid_index(prev_index) else None

        # Next (unit of time), skipping over empty (unit of time).
        next_index = this_index + 1
        next_link = self.dates_list[next_index] if self.is_valid_index(next_index) else None

        return prev_link, this_link, next_link

    def is_valid_index(self, index):
        return (0 <= index) and (index < len(self.dates_list))



class ArchiveYearView(TemplateView):
    template_name = "blog/archive_year.html"

    def get_context_data(self, **kwargs):
        year = self.kwargs["year"]

        posts_list = Post.objects.filter(
            created_on__year = year
            ).order_by("created_on")

        search_results = posts_list.annotate(month=TruncMonth("created_on"))
        cal = BlogHTMLCalendar(year, posts_list).printyear()

        # Output to Template
        prev_link, this_link, next_link = self.get_prev_and_next(year)

        context = {
            "site_title": '| {}'.format(year),
            "page_obj": search_results,
            "prev_year": prev_link,
            "this_year": this_link,
            "next_year": next_link,
            "cal": cal
        }
        return context
    
    def get_prev_and_next(self, year):
        """
        prev_link, this_link, next_link are lists of [year].
        Access the integer through list index 0.
        """
        # This section slightly differs depending on type of archive.
        dates = Post.objects.dates("created_on", "year", "ASC")
        self.dates_list = [[date.year] for date in dates]
        this_link = [year]

        # The rest of this section is the same.
        this_index = self.dates_list.index(this_link)

        # Previous (unit of time), skipping over empty (unit of time).
        prev_index = this_index - 1
        prev_link = self.dates_list[prev_index] if self.is_valid_index(prev_index) else None

        # Next (unit of time), skipping over empty (unit of time).
        next_index = this_index + 1
        next_link = self.dates_list[next_index] if self.is_valid_index(next_index) else None

        return prev_link, this_link, next_link

    def is_valid_index(self, index):
        return (0 <= index) and (index < len(self.dates_list))



class ArchiveView(TemplateView):
    template_name = "blog/archive.html"

    def get_context_data(self, **kwargs):
        dates = Post.objects.dates("created_on", "year", "DESC")
        years = [date.year for date in dates]

        # Output to Template
        context = {
            "site_title": '| Archives',
            "page_title": '<h2>Archives</h2>',
            "years": years
        }
        return context



