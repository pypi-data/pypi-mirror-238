from django.db import models
from django.conf import settings

ENV = getattr(settings, "ENVIRONMENT", "LOCALHOST")
database_type = getattr(settings, "database_type", "sqlite3")

try:
    # necessary if this is being called from wall_e and therefore the settings need to be picked up from
    # django_settings instead of the settings file in the wall_e_models repo
    import django_settings
    ENV = getattr(django_settings, "ENVIRONMENT", "LOCALHOST")
    database_type = getattr(django_settings, "database_type", "sqlite3")
except ModuleNotFoundError:
    pass


class GeneratedIdentityField(models.AutoField):
    description = "An Integer column which uses `GENERATED {ALWAYS | BY DEFAULT} AS IDENTITY`. \
                  A modern alternative to `BIGSERIAL` from the SQL standard."

    def __init__(self, *args, **kwargs):

        # this is necessary because of the `always` that was used in the fourth migration
        kwargs.pop('always', None)

        # have to do it like this cause otherwise loaddata will not work when loading datat from PROD,
        # you wind up with the error
        # DETAIL:  Column "ban_id" is an identity column defined as GENERATED ALWAYS.
        # HINT:  Use OVERRIDING SYSTEM VALUE to override.
        self.always = ENV == "PRODUCTION"

        super(GeneratedIdentityField, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['always'] = self.always
        return name, path, args, kwargs

    def db_type(self, connection):
        if database_type == "postgresSQL":
            return f"INTEGER GENERATED {'ALWAYS' if self.always else 'BY DEFAULT'} AS IDENTITY"
        else:
            # migration 4 gives this error unless the db_type is just INTEGER
            #   File "python3.9/site-packages/django/db/backends/utils.py", line 82, in _execute
            #     return self.cursor.execute(sql)
            #   File "python3.9/site-packages/django/db/backends/sqlite3/base.py", line 421, in execute
            #     return Database.Cursor.execute(self, query)
            # sqlite3.OperationalError: near "AS": syntax error
            return "INTEGER"
            # apparently, sqlite3 automatically set the definition of the field to
            # INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT
