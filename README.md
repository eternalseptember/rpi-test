# rpi-test

Test pulling a Django project from GitHub to the Raspberry Pi. Specifically, to make sure settings are set and hidden correctly, so that when I pull my project from Github, the "dev" credentials from desktop/laptop don't break the "prod" crendentials on the Pi, and the Django project can be updated after migrating database changes and reloading the daemon and gunicorn service.

No passwords or secret keys that are exposed on this repo are "real". They're test values for test reasons.

## Solution That Works for Me So Far

Created a `.env` file, added it to `.gitignore`, and used [Python Decouple](https://pypi.org/project/python-decouple/) to get settings for `personal_blog/settings.py`. The Pi has its own `.env` file with its own settings.

## Blog Tutorial

The foundation of this blog project began from [this tutorial](https://realpython.com/build-a-blog-from-scratch-django/#start-your-django-project), which I'll be using as an inspiration for my personal blog project. I did not implement the comments section.

### Additional Changes

* In `settings.py`, set the `TIME_ZONE`, and added `APPEND_SLASH = True`.
* In the `TEMPLATES` -> `OPTIONS` section of `settings.py`, set `autoescape = False` and added `highlighter` and `month_name` template tags.
    * Turning off autoescape shouldn't be done for projects that will be hosted on the internet with other users, but this project is ultimately going to be hosted on an internal raspberry pi where I'm going to be the only user.
* Implemented static files for css and javascript.
* Enabled image upload to the media folder.
* Added a description field to categories and updated the category form accordingly.
* Registered models to the admin panel using the decorator instead of the object.
* Made the views output some routine HTML (like site and page titles) in order to reduce the number of template HTML files to manage.

### Admin Panel

* Centered the admin panel.
* Centered the change form action buttons.
* Put messagelist on fixed position to the bottom so that it removes itself from the flexbox calculations, so the create/edit a post form stays in place after submitting a post.
* Categories and posts lists are paginated.

#### CategoryAdmin

* Categories list is alphabetized and shows the number of posts in that category, and both columns are sortable.
* The edit view of a category has the list of posts in that category, and each post is a link to that post's edit page.
* In the category admin and in a category's edit page, there's a link to that category's public detail page.
* In a category's public detail page, there is a link to the category's admin edit page.
* Created custom template tags for highlighting search results and converting integer to month names.

#### PostAdmin

* Display each post's dates created and modified in the admin panel (which made those sections sortable), and defaults to listing posts by creation date in descending order.
* Added a search for the post's title and filters on dates.
* Moved the change form actions to the bottom.
* In the post admin and in a post's edit page, there's a link to that post's public detail page.
* In a post's public detail page, there is a link to the post's admin edit page.
* In the add/edit a post admin page, resized the title widget and separated the categories list.
* Made the created_on date/time editable fields, with the current date/time as the default, and made the datetime widget into a single line.
* Markdown editor with [Markdownx](https://neutronx.github.io/django-markdownx/installation/) in the body of the post, and made the preview collapsible.

### Other Features

* Toggle light and dark modes, and the choice is saved in a localsession cookie.
* Basic search query (full-text search with postgres in the post's title **or** body) is highlighted.
* Basic search results are paginated.
* Pagination on the index and category pages.
* Next/Prev links on each entry's page.
* The title of each entry's page is a link to its admin edit page.
* The title of each category's page is a link to its admin edit page.
* Archives:
    * `/archive/YYYY/` is the yearly archive index. It has that year's calendar printed and then an index listing all of the posts made in that year. The calendar's year header is a link to the page itself, the month headings are links to that month's index of posts (if available), and the days are links to that day's post archives (if available). There is custom yearly pagination for going to the previous and next years that there are posts for.
    * `/archive/YYYY/MM/` is the index listing all of the posts made in that month. There is custom monthly pagination for going to the previous and next months that there are posts for.
    * `/archive/YYYY/MM/DD` or `/archive/YYYY/M/D` is all of the posts made on that day. There is custom daily pagination for going to the previous and next days that there are posts for.
* Advanced search page powered by [django-filter](https://django-filter.readthedocs.io/en/stable/index.html).
    * **NOTE:** Queries on the title and body (as well as other fields) are joined by **and**.
    * Empty or invalid filters *don't* show every post!
    * Posts' title and body queries are highlighted.
    * Got rid of the error messages and only made the input box's outline red if there's an error.
    * Can search by date on a DateTime field, but the input has to be in month/day/year order, i.e. any combination of `MM/DD/YYYY` or `M/D/YYYY`.
    * Can search for posts made on an anniversary date (the year input is ignored).
    * Can search by category tag, and searched tags are highlighted.
    * A checkbox to search the categories with boolean `AND` (i.e. search for posts with all selected tags) instead of the default `OR`.
    * A dropdown box to choose whether to sort results by date.
    * Advanced search results are paginated with the [{% querystring %}](https://docs.djangoproject.com/en/5.1/ref/templates/builtins/#dynamic-usage) template tage.
    * Clicking on the "Advanced Search" title toggles the visibility of the advanced search form, and the state is saved in a localstorage cookie so that the toggle state is maintained while navigating search results.
    * The reset button returns the form to the values it had before, so if the form had submitted search results (which means those input fields have their attr `value`s set), clicking "reset" will return the form to the `value`s set. Clicking the "Search" link at the top gets the empty, clear form.

## Things I've Ruled Out

* CKEditor. Not only is there an annoying message that says the package is unsupported and has security vulnerabilities, but I'm not looking for a fully-featured editor that is going to be a pain to configure. I need a way to manage image uploads, and I'll be happy with a markdown editor that plays well with the Django admin panel.

## Problems I Had

### Markdown was not Displaying Images

I followed the steps to install and add Markdownx to the project, and was able to get images uploaded and shown in the preview, but after the post was made, the image was not rendered. Instead, a markdown code with the image path was displayed instead.

The solution was to create a property in the model that applies `markdownify` onto the post, and then render that property in the template.

In `models.py`:

```
from markdownx.utils import markdownify

# In the class with the markdown object:
    @property
    def formatted_markdown(self):
        return markdownify(self.body)
```

In the index template:

```
<p>{{ post.formatted_markdown | safe }}</p>
```

#### Sources (because we're all victims of Google's personalized search algorithms):

* [I can't understand the django-markdownx's usage](https://stackoverflow.com/questions/42416123/i-cant-understand-the-django-markdownxs-usage/42418210#42418210) Search result I found on duckduckgo.
* [How to Render Markdown Content in Django](https://bastakiss.com/blog/django-6/how-to-render-markdown-content-in-django-388) Search result I found on duckduckgo.
* [How to Use Django-Markdownx for Your Blog](https://blog.existenceundefined.com/2023/07/test.html) Google gives me this search result a week after I resolved this issue, while researching a different problem (how to customize markdownxadminpanel).

#### Note

I have since turned off autoescape in `settings.py` (because this is intended to be a personal project hosted on a LAN where I'm the only user), so I have removed the `| safe` filters from my templates.

### Stray Paragraph Tag

While messing with CKEditor and Markdownx, posts started rendering with an extra paragraph tag at the very beginning, and browsers try to complete it by ending it with a paragraph tag somewhere. There was an extra `<p>` at the very beginning of the post body, so the browser adds a closing `</p>` there, and for some reason, there's another set of `<p></p>` at the very end of the post body? This is a consequence of both Markdown and CKEditor... html generation quirks.

The css solution of

```
p:empty {
    display:none;
}
```

didn't work for me, so I used jquery instead, placing it in the base template.

```
$(document).ready(function(){
    $('p:empty').remove();
});
```

### Trying to Filter on a DateTime Field with Only Date with Django Filters

`date`, `date__gt` (and `date__gte`), `date__lt` (and `date__lte`) extracts the date from a datetime field.

Here's my `filters.py`:

```
from blog.models import Post
import django_filters


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = {
            "title": ['icontains'],
            "body": ['icontains'],
            "created_on": ['date', 'date__gte', 'date__lte'],
            }
```

### Advanced Search Page Shows *EVERYTHING* Instead of *NOTHING* When Invalid or No Filters Applied

In order to achieve the desired result of showing *NOTHING* instead of *EVERYTHING* when there are no or invalid filters, both of these steps had to be done:

#### Invalid Filter

Overriding this filter (in `filters.py`) will make the queryset return nothing instead of everything if there is an invalid filter.

```
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
```

#### No Filters (Like When Loading the Search Page for the First Time)

In the associated view (in  `views.py`), I checked if there is a request. Need to update the field names if filters are added/deleted/changed.

```
    s1 = request.GET.get("title__icontains")
    s2 = request.GET.get("body__icontains")
    s3 = request.GET.get("created_on__date")
    s4 = request.GET.get("created_on__date__gte")
    s5 = request.GET.get("created_on__date__lte")

    if s1 or s2 or s3 or s4 or s5:
        search_results = post_filter.qs
    else:
        search_results = Post.objects.none()
```

### Autoescape:False Seemingly Being Ignored

 In the advanced search page, the search results' title and body are highlighted if they match the searched term. However, if the advanced search did not include a search of the body text, then the body of the search results were escaped, even with `TEMPLATES.OPTIONS autoescape': False` in `settings.py`.

Since the `query_body` (and `query_title`) were sent in the context for highlighting:

```
    context = {
        "site_title": '<title>My Personal Blog | Advanced Search</title>',
        "page_title": '<h2>Advanced Search</h2>',
        "form": post_filter.form,
        "page_obj": page_obj,
        "query_title": s1,  # for highlighting
        "query_body": s2,  # for highlighting
    }
```

The solution was adding a check in the template to see if the returned `query_body` had anything. This is the same `s1` and `s2` referenced in the previous solution to show no search results if there are no search filters applied.

```
        {% if query_body %}
            <p>{{ post.formatted_markdown | highlighter:query_body }}</p>
        {% else %}
            <p>{{ post.formatted_markdown }}</p>
        {% endif %}
```

### How to Pass a Request to a Filter (django_filters.FilterSet)

`selected_categories` is a multiple choice field where many choices can be selected at once. If I attempt to access it in the view with `request.GET.get("categories")`, then I will only get a single value, the most recent value clicked.

In order to get all of the selected options, use `request.GET.getlist("categories")`.
