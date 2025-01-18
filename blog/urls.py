from django.urls import path
from . import views

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("category/<category>/", views.blog_category, name="blog_category"),
    path("search/", views.blog_search, name="blog_search"),
    path("archive/<int:year>/<int:month>/<int:day>/", views.ArchiveDayView.as_view(), name="archive_day"),
    path("archive/<int:year>/<int:month>/", views.ArchiveMonthView.as_view(), name="archive_month"),
    path("archive/<int:year>/", views.ArchiveYearView.as_view(), name="archive_year"),
    path("archives/", views.ArchiveView.as_view(), name="blog_archives"),
]

