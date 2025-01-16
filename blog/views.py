from django.shortcuts import render
from blog.models import Post, Category
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic.base import TemplateView
from datetime import date, datetime
from django.db.models.functions import TruncMonth
from blog.custom_calendar import BlogHTMLCalendar


def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj
    }
    return render(request, "blog/index.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains = category
        ).order_by("-created_on")

    category = Category.objects.get(name=category)

    paginator = Paginator(posts, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "category": category,
        "page_obj": page_obj,
    }
    return render(request, "blog/category.html", context)


def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)
    context = {
        "post": post,
    }
    return render(request, "blog/detail.html", context)


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

    context = {
        "query": query,
        "page_obj": page_obj,
    }
    return render(request, "blog/search.html", context)


class ArchiveDayView(TemplateView):
    template_name = "blog/archive_day.html"

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

        context = {
            "date": day_date,
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

        context = {
            "date": date(year, month, 1),
            "page_obj": search_results,
        }
        return context


class ArchiveYearView(TemplateView):
    template_name = "blog/archive_year.html"

    def get_context_data(self, *args, **kwargs):
        year = self.kwargs["year"]

        search_results = Post.objects.filter(
            created_on__year = year
            ).order_by("created_on") \
            .annotate(month=TruncMonth("created_on"))

        context = {
            "year": year,
            "page_obj": search_results,
        }
        return context


class ArchiveView(TemplateView):
    template_name = "blog/archive.html"

    def get_context_data(self, **kwargs):
        year = datetime.now().year
        cal = BlogHTMLCalendar(year).formatyear()

        context = {
            "cal": cal
        }
        return context



