# rpi-test

Test pulling a django project from git to the raspberry pi. Specifically, to make sure settings are set and hidden correctly, so that when I pull a project from github, the "dev" credentials from desktop/laptop don't break the "prod" crendentials on the pi, and the django project can be updated after reloading daemon and gunicorn service.

No passwords or secret keys that are exposed on this repo are "real". They're test values for test reasons.
