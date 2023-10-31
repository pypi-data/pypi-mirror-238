===============
wall_e_models
===============

wall_e_models is a Django app to manage the database for CSSS's discord bot wall_e.

Quick start
-----------

1. Add "wall_e_models" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...,
        "wall_e_models",
    ]

2. Run ``python manage.py migrate`` to create the wall_e models.