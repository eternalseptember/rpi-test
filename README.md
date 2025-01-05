# rpi-test

Test pulling a Django project from GitHub to the Raspberry Pi. Specifically, to make sure settings are set and hidden correctly, so that when I pull my project from Github, the "dev" credentials from desktop/laptop don't break the "prod" crendentials on the Pi, and the Django project can be updated after migrating database changes and reloading the daemon and gunicorn service.

No passwords or secret keys that are exposed on this repo are "real". They're test values for test reasons.

## Solution That Works for Me So Far

Created a `.env` file, added it to `.gitignore`, and used [Python Decouple](https://pypi.org/project/python-decouple/) to get settings for `personal_blog/settings.py`. The Pi has its own `.env` file with its own settings.

## Tutorial

Project is based on [this tutorial](https://realpython.com/build-a-blog-from-scratch-django/#start-your-django-project) that I'll be using as an inspiration for my personal blog project.

Changes from the tutorial:

* Did not implement the comments section.
* Implemented static files for css.
* Centered the admin panel.

Things that I will eventually experiment with:

* Should probably limit how many posts show on the front page, with forward and backward navigation links.
* Rich-text editor, with image-uploading capabilities.
* Commented out section for media files. Haven't tested that functionality yet.
