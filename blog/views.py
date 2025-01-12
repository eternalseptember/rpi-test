from django.shortcuts import render
from blog.models import Post
from django.core.paginator import Paginator
from django.db.models import Q


def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }
    return render(request, "blog/index.html", context)


def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
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


def search(request):
    query = request.GET.get('q')
    if query:
        search_results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query)
        ).distinct().order_by("-created_on")

    else:
        search_results = Post.objects.none()

    paginator = Paginator(search_results, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'query': query,
        'page_obj': page_obj,
    }
    return render(request, 'blog/search.html', context)


