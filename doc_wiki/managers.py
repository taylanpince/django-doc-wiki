import os

from datetime import datetime, timedelta

from django.db import models

from doc_wiki import settings


class WikiPageQuerySet(models.query.QuerySet):
    """
    A custom QuerySet that can update the model instance from a file
    """
    def update(self, obj):
        """
        If the object needs to be updated, gets the data from local file and
        saves the new data
        """
        if obj.pk and obj.timestamp:
            if os.path.exists(obj.path):
                if os.path.getmtime(obj.path) == obj.timestamp:
                    return obj
            else:
                obj.delete()
                
                raise self.model.DoesNotExist("%s matching query does not exist" % self.model._meta.object_name)

        try:
            handle = open(obj.path, "r")
            content = handle.read()
            handle.close()
        except IOError:
            raise self.model.DoesNotExist("%s matching query does not exist" % self.model._meta.object_name)

        obj.content = content
        obj.timestamp = os.path.getmtime(obj.path)

        obj.save()

        return obj


    def get(self, *args, **kwargs):
        """
        Tries to get the object from the DB, if the object cannot be found,
        tries to find it in the local directory
        """
        try:
            obj = super(WikiPageQuerySet, self).get(*args, **kwargs)
            
            return self.update(obj)
        except self.model.DoesNotExist:
            pass

        slug = kwargs.get("slug", None)
        path = os.path.join(settings.DIRECTORY_PATH, slug)

        if slug and os.path.exists(path):
            obj = self.model()

            obj.slug = slug
            obj.path = path

            return self.update(obj)
        else:
            raise self.model.DoesNotExist("%s matching query does not exist" % self.model._meta.object_name)


class WikiPageManager(models.Manager):
    def get_query_set(self):
        return WikiPageQuerySet(model=self.model, query=None)
