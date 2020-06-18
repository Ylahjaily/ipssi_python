from django.db import models


class AdOfferManager(models.Manager):
    def get_queryset(self):
        return super(AdOfferManager, self).get_queryset().filter(
            type='offer',
        )


class AdRequestManager(models.Manager):
    def get_queryset(self):
        return super(AdRequestManager, self).get_queryset().filter(
            type='request',
        )

