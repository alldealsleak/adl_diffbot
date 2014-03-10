from django.db import models


class Media(models.Model):
    caption = models.CharField(max_length=50, blank=True)
    link = models.URLField(max_length=500)

    class Meta:
        verbose_name_plural = 'Media'

    def __unicode__(self):
        return '{} - {}'.format(self.caption, self.link)


class Product(models.Model):
    product_id = models.CharField(max_length=50)
    link = models.URLField(max_length=500)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    offer_price = models.FloatField(blank=True, null=True)
    regular_price = models.FloatField(blank=True, null=True)
    merchant = models.CharField(max_length=20, blank=True)
    media = models.ForeignKey('Media', blank=True, null=True)

    def __unicode__(self):
        return '{} - {}'.format(self.product_id, self.title)


