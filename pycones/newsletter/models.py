# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
import uuid

#def get_or_create_active_newsletter():
#    current_active_nl = getattr(settings, 'ACTIVE_NEWSLETTER', '2013')
#    try:
#        newsletter = Newsletter.objects.get(name=current_active_nl)
#    except Newsletter.DoesNotExist:
#        newsletter = Newsletter.objects.create(name=current_active_nl)
#
#    return newsletter


class ArticleManager(models.Manager):

    def get_last_articles(self):
        """
        Method to get last 5 articles added to active newsletter
        """
        article_queryset = super(ArticleManager,self).get_query_set()
        articles = article_queryset\
            .filter(visible=True)\
            .order_by('-created_date')[:5]

        return articles

    def get_articles_per_page(self, page_number):
        """
        Method to get 5 articles per page number( 5 articles per page )
        For example:
            if page=1 articles 6-10
            if page=2 articles 11-15
        To calculate first article we use: 5 * page_number + 1
        To calculate last article we use: first_article + 4
        """

        # FIXME: use django pagination instead of manual pagination
        first_article = (page_number * 5 + 1)
        last_article = (first_article + 4)

        queryset = super(ArticleManager,self).get_query_set()

        articles = queryset\
            .filter(visible=True)\
            .order_by('-created_date')[first_article:last_article]

        return articles

    def get_articles_per_year(self,year):
        """
        Method to get articles per year
        """
        queryset = super(ArticleManager,self).get_query_set()

        articles = queryset.filter(
                    visible=True,
                    created_date__year=year)\
                    .order_by('-created_date')

        return articles

    def get_articles_per_month(self):
        """
        Method to get articles per year and month
        """
        queryset = super(ArticleManager,self).get_query_set()
        articles = queryset.filter(
                        visible=True,
                        created_date__year=year, created_date__month=month)\
                    .order_by('-created_date')

        return articles


class Article(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=False, unique=True, null=False)
    text = models.TextField()
    created_date = models.DateTimeField(editable=False, auto_now_add=True)
    updated_date = models.DateTimeField(editable=False, auto_now=True)
    visible = models.BooleanField(default=False)
    order = models.IntegerField(blank=True, null=True)

    objects = ArticleManager()

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["order"]

    def get_absolute_url(self):
        current_site = Site.objects.get_current()
        url = reverse('newsletter:article', args=[self.slug])
        return 'http://%s%s' % (current_site.domain, url)


class Newsletter(models.Model):
    uuid = models.CharField(max_length=255, default=lambda: str(uuid.uuid1()))
    title = models.CharField(max_length=255)
    head = models.TextField()
    created_date = models.DateTimeField(editable=False, auto_now_add=True)
    articles = models.ManyToManyField("Article")
    sent = models.BooleanField(default=False)
    sent_date = models.DateTimeField(editable=False, auto_now=True)


    def __unicode__(self):
        return u"{0} ({1})".format(self.title,str(self.created_date)[:7])

    class Meta:
        ordering = ["created_date"]

    def get_absolute_url(self):
        current_site = Site.objects.get_current()
        url = reverse('newsletter:newsletter', args=[self.uuid])
        return 'http://%s%s' % (current_site.domain, url)

class Subscription(models.Model):
    user_email = models.EmailField()
    val_token = models.CharField(max_length=128)
    admin = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user_email


