from django.db import models
from django.utils.encoding import smart_str


COUNTRY_CHOICES = (
    ('sg', 'Singapore'),
    ('vn', 'Vietnam'),
)

class Company(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Companies'

    def __unicode__(self):
        return '{}'.format(self.name)


class Category(models.Model):
    name = models.CharField(max_length=20)
    depth = models.IntegerField(default=0)
    children = models.ManyToManyField(
        'Category', symmetrical=False, blank=True)

    def __unicode__(self):
        s = ''
        for i in range(0, self.depth):
            s += '---'
        return '{}{}'.format(s, self.name)

    def get_children(self):
        return self.children.all()


class CurrentUrl(models.Model):
    company = models.ForeignKey('Company')
    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    category = models.ForeignKey('Category', blank=True, null=True)
    merchant = models.CharField(max_length=20, blank=True)
    link = models.URLField()
    added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{} - {}'.format(self.company.name, self.link)
        

class Media(models.Model):
    caption = models.CharField(max_length=500, blank=True)
    link = models.URLField(max_length=500)

    class Meta:
        verbose_name_plural = 'Media'

    def __unicode__(self):
        return '{} - {}'.format(self.caption, self.link)


class Product(models.Model):
    product_id = models.CharField(max_length=100)
    link = models.URLField(max_length=500)
    title = models.CharField(max_length=200)
    category = models.ForeignKey('Category', blank=True, null=True)
    description = models.TextField(blank=True)
    offer_price = models.FloatField(blank=True, null=True)
    regular_price = models.FloatField(blank=True, null=True)
    merchant = models.CharField(max_length=50, blank=True)
    media = models.ForeignKey('Media', blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ProductSingapore(Product):
    company = models.ForeignKey('Company')

    def __unicode__(self):
        return '{} - {}'.format(self.product_id, smart_str(self.title))


class ProductVietnam(Product):
    company = models.ForeignKey('Company')

    def __unicode__(self):
        return '{} - {}'.format(self.product_id, smart_str(self.title))


