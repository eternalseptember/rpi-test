from blog.calendar import BlogHTMLCalendar
from blog.models import Post, Category
from datetime import date, datetime
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.functions import TruncMonth, ExtractYear
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView


def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Output to Template
    site_title = '<title>My Personal Blog</title>'

    context = {
        "site_title": site_title,
        "page_obj": page_obj
    }
    return render(request, "blog/index.html", context)



def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains = category
        ).order_by("-created_on")

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Output to Template
    category = Category.objects.get(name=category)
    site_title = '<title>My Personal Blog | Category: {}</title>'.format(category)
    category_edit_url = reverse("admin:{}_{}_change"
                  .format(category._meta.app_label, category._meta.model_name), 
                  args=[category.id])
    page_title = '<h2>category: <a href="{}">{}</a></h2>'.format(category_edit_url, category)
    page_title += '<span class="category_description">{}</span>'.format(category.description)

    context = {
        "site_title": site_title,
        "page_title": page_title,
        "page_obj": page_obj,
    }
    return render(request, "blog/index.html", context)



def blog_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)

        # Output to Template
        site_title = '<title>My Personal Blog | {}</title>'.format(post.title)
        post_edit_url = reverse("admin:{}_{}_change"
                  .format(post._meta.app_label, post._meta.model_name), 
                  args=[post.pk])
        page_title = '<h2><a href="{}">{}</a></h2>'.format(post_edit_url, post.title)

        context = {
            "site_title": site_title,
            "page_title": page_title,
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
    site_title = '<title>My Personal Blog | Search: {}</title>'.format(query)
    page_title = '<h2>search: {}</h2>'.format(query)

    context = {
        "site_title": site_title,
        "page_title": page_title,
        "page_obj": page_obj,
    }
    return render(request, "blog/search.html", context)



class ArchiveDayView(TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, *args, **kwargs):
        year = self.kwargs["year"]
        month = self.kwargs["month"]
        day = self.kwargs["day"]
        day_date = date(year, month, day)

        search_results = Post.objects.filter(
            created_on__date = day_date
            ).order_by("-created_on")

        # This is paginated because of test data entry.
        # This will not be paginated on the real project.
        paginator = Paginator(search_results, 5)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Output to Template
        site_title = '<title>My Personal Blog | {}</title>'.format(day_date.strftime("%b %-d, %Y"))
        page_title = '<h2>{}</h2>'.format(day_date.strftime("%b %-d, %Y"))

        context = {
            "site_title": site_title,
            "page_title": page_title,
            "page_obj": page_obj,
        }
        return context



class ArchiveMonthView(TemplateView):
    template_name = "blog/archive_month.html"

    def get_context_data(self, *args, **kwargs):
        year = self.kwargs["year"]
        month = self.kwargs["month"]

        search_results = Post.objects.filter(
            created_on__year = year,
            created_on__month = month
            ).order_by("-created_on")

        # Output to Template
        month_date = date(year, month, 1)
        site_title = '<title>My Personal Blog | {}</title>'.format(month_date.strftime("%B %Y"))
        page_title = '<h2>{}</h2>'.format(month_date.strftime("%B %Y"))

        context = {
            "site_title": site_title,
            "page_title": page_title,
            "page_obj": search_results,
        }
        return context



class ArchiveYearView(TemplateView):
    template_name = "blog/archive_year.html"

    def get_context_data(self, *args, **kwargs):
        year = self.kwargs["year"]

        posts_list = Post.objects.filter(
            created_on__year = year
            ).order_by("created_on")

        search_results = posts_list.annotate(month=TruncMonth("created_on"))
        cal = BlogHTMLCalendar(year, posts_list).printyear()

        # Output to Template
        site_title = '<title>My Personal Blog | {}</title>'.format(year)
        prev_year, next_year = self.get_next_and_prev(year)

        context = {
            "site_title": site_title,
            "page_obj": search_results,
            "prev_year": prev_year,
            "next_year": next_year,
            "cal": cal
        }
        return context
    
    def get_next_and_prev(self, year):
        dates = Post.objects.dates("created_on", "year", "ASC")
        years = [date.year for date in dates]
        this_year_index = years.index(year)

        # Previous Year
        prev_index = this_year_index - 1
        if (0 <= prev_index) and (prev_index < len(years)):
            prev_year = years[prev_index]
        else:
            prev_year = None

        # Next year
        next_index = this_year_index + 1
        if (0 <= next_index) and (next_index < len(years)):
            next_year = years[next_index]
        else:
            next_year = None

        return prev_year, next_year



class ArchiveView(TemplateView):
    template_name = "blog/archive.html"

    def get_context_data(self, **kwargs):
        dates = Post.objects.dates("created_on", "year", "DESC")
        years = [date.year for date in dates]

        # Output to Template
        site_title = '<title>My Personal Blog | Archives</title>'
        page_title = '<h2>Archives</h2>'

        context = {
            "site_title": site_title,
            "page_title": page_title,
            "years": years
        }
        return context



