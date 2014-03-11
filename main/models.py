from django.db import models


COUNTRY_CHOICES = (
    ('sg', 'Singapore'),
)

class Company(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __unicode__(self):
        return '{}'.format(self.name)


class CurrentUrl(models.Model):
    company = models.ForeignKey(Company)
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    link = models.URLField()
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{} - {}'.format(self.company.name, self.link)    


class Media(models.Model):
    caption = models.CharField(max_length=50, blank=True)
    link = models.URLField(max_length=500)

    class Meta:
        verbose_name_plural = 'Media'

    def __unicode__(self):
        return '{} - {}'.format(self.caption, self.link)


class Product(models.Model):
    product_id = models.CharField(max_length=100)
    link = models.URLField(max_length=500)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    offer_price = models.FloatField(blank=True, null=True)
    regular_price = models.FloatField(blank=True, null=True)
    merchant = models.CharField(max_length=20, blank=True)
    media = models.ForeignKey('Media', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProductSingapore(Product):
    company = models.ForeignKey('Company')

    def __unicode__(self):
        return '{} - {}'.format(self.product_id, self.title)






