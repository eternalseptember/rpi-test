# rpi-test

Test pulling a Django project from GitHub to the Raspberry Pi. Specifically, to make sure settings are set and hidden correctly, so that when I pull my project from Github, the "dev" credentials from desktop/laptop don't break the "prod" crendentials on the Pi, and the Django project can be updated after migrating database changes and reloading the daemon and gunicorn service.

No passwords or secret keys that are exposed on this repo are "real". They're test values for test reasons.

## Solution That Works for Me So Far

Created a `.env` file, added it to `.gitignore`, and used [Python Decouple](https://pypi.org/project/python-decouple/) to get settings for `personal_blog/settings.py`. The Pi has its own `.env` file with its own settings.

## Blog Tutorial

The foundation of this blog project is started from [this tutorial](https://realpython.com/build-a-blog-from-scratch-django/#start-your-django-project), which I'll be using as an inspiration for my personal blog project. I did not implement the comments section.

### Additional Changes

* Set the `TIME_ZONE` in `settings.py`.
* Implemented static files for css and javascript.
* Enabled image upload to the media folder.
* Added a description field to categories and updated the category template accordingly.
* Registered models to the admin panel using the decorator instead of the object.

### Admin Panel

* Centered the admin panel.
* Centered the change form action buttons.
* Put messagelist on fixed position to the bottom so that it removes itself from the flexbox calculations, so the create/edit a post form stays in place after submitting a post.
* Categories and posts lists are paginated.

#### CategoryAdmin

* Categories list is alphabetized and shows the number of posts in that category, and both columns are sortable.
* The change view of a category has the list of posts in that category, and each post is a link to that post's edit page.

#### PostAdmin

* Display each post's dates created and modified in the admin panel (which made those sections sortable), and defaults to listing posts by creation date in descending order.
* Added a search for the post's title and filters on dates.
* Moved the change form actions to the bottom.
* In the post admin and in a post's edit page, there's a link to that post's public detail page.
* In the add/edit a post admin page, resized the title widget and separated the categories list.
* Made the created_on date/time editable fields, with the current date/time as the default, and made the datetime widget into a single line.
* Markdown editor with [Markdownx](https://neutronx.github.io/django-markdownx/installation/) in the body of the post, and made the preview collapsible.

### Other Features

* Pagination on the index page and category page.
* Next/Prev links on each entry's page.
* The title of each entry's page is a link to its admin change page.
* Paginated search results.
* Archives page with links to the following archives... That are mostly here for testing convenience:
    * Paginated daily post archives at `/archive/YYYY/MM/DD` or `/archive/YYYY/M/D`.
    * Monthly index of posts (date and post titles only) at `/archive/YYYY/MM/`.
    * Yearly index of posts (date and post titles only), with month headings, at `/archive/YYYY/`.
        * Haven't actually created data across multiple months yet.

### Things that I will eventually experiment with

* Search posts by date and/or date range.

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
