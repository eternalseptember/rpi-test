# rpi-test

Test pulling a Django project from GitHub to the Raspberry Pi. Specifically, to make sure settings are set and hidden correctly, so that when I pull my project from Github, the "dev" credentials from desktop/laptop don't break the "prod" crendentials on the Pi, and the Django project can be updated after migrating database changes and reloading the daemon and gunicorn service.

No passwords or secret keys that are exposed on this repo are "real". They're test values for test reasons.

## Solution That Works for Me So Far

Created a `.env` file, added it to `.gitignore`, and used [Python Decouple](https://pypi.org/project/python-decouple/) to get settings for `personal_blog/settings.py`. The Pi has its own `.env` file with its own settings.

## Blog Tutorial

The foundation of this blog project is based on [this tutorial](https://realpython.com/build-a-blog-from-scratch-django/#start-your-django-project), which I'll be using as an inspiration for my personal blog project. I did not implement the comments section.

In addition:

* Set the time_zone in `settings.py`.
* Implemented static files for css and javascript.
* Centered the admin panel.
* Put messagelist on fixed position to the bottom so that it removes itself from the flexbox calculations, so the create/edit a post form stays in place after submitting a post.
* Made the date and time editable fields, and made the datetime widget into a single line.
* Markdown editor with [Markdownx](https://neutronx.github.io/django-markdownx/installation/) in the body of the post, and made the preview collapsible.
* Enabled image upload to the media folder.
* Pagination on the index page.

Things that I will eventually experiment with:

* next/prev links on each entry's page.
* pagination on the category page.

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

More info [here](https://stackoverflow.com/questions/42416123/i-cant-understand-the-django-markdownxs-usage/42418210#42418210) and [here](https://bastakiss.com/blog/django-6/how-to-render-markdown-content-in-django-388).

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
