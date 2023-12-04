from django.db import models
from django.db.models.query import QuerySet


class BaseQuerySet(models.QuerySet):
    """Base QuerySet"""

    pass


class BaseManager(models.Manager):
    """Base Manager"""

    def get_queryset(self) -> QuerySet:
        return BaseQuerySet(model=self.model, using=self._db)


class BaseModel(models.Model):
    """Base Model"""

    objects = BaseManager()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("created",)
