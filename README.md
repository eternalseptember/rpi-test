# rpi-test

Test pulling a Django project from GitHub to the Raspberry Pi. Specifically, to make sure settings are set and hidden correctly, so that when I pull my project from Github, the "dev" credentials from desktop/laptop don't break the "prod" crendentials on the Pi, and the Django project can be updated after migrating database changes and reloading the daemon and gunicorn service.

No passwords or secret keys that are exposed on this repo are "real". They're test values for test reasons.

## Solution That Works for Me So Far

Created a `.env` file, added it to `.gitignore`, and used [Python Decouple](https://pypi.org/project/python-decouple/) to get settings for `personal_blog/settings.py`. The Pi has its own `.env` file with its own settings.

## Blog Tutorial

The foundation of this blog project is based on [this tutorial](https://realpython.com/build-a-blog-from-scratch-django/#start-your-django-project), which I'll be using as an inspiration for my personal blog project. I did not implement the comments section.

In addition:

* Implemented static files for css and javascript.
* Centered the admin panel.
* Put messagelist on fixed position to the bottom so that it removes itself from the flexbox calculations, so the create/edit a post form stays in place after submitting a post.
* Markdown editor with [Markdownx](https://neutronx.github.io/django-markdownx/installation/) in the body of the post.
* Enabled image upload to the media folder.

Things that I will eventually experiment with:

* Limiting how many posts show on the front page, with forward and backward navigation links.

## Things I've Ruled Out

* CKEditor. Not only is there an annoying message that says the package is unsupported and has security vulnerabilities, but I'm not looking for a fully-featured editor that is going to be a pain to configure. I need a way to manage image uploads, and I'll be happy with a markdown editor that plays well with the Django admin panel.

## Problems I Had

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
