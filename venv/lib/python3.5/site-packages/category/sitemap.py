#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
      possible values for changefreq:
        'always'
        'hourly'
        'daily'
        'weekly'
        'monthly'
        'yearly'
        'never'
"""

from datetime import datetime, timedelta

from django.utils import timezone
from django.contrib.sitemaps import Sitemap
# from django.db.models import Max

from category.models import Category, Tag


class CategorySitemap(Sitemap):
    """
    SiteMap for Categories
    """

    def changefreq(self, obj):
        return "weekly"

    def priority(self, obj):
        return 1.0

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return datetime.now()


class TagSitemap(Sitemap):
    """
    SiteMap for Tags
    """

    def changefreq(self, obj):
        if obj.touched > timezone.now()-timedelta(hours=1):
            return "hourly"
        if obj.touched > timezone.now()-timedelta(days=1):
            return "daily"
        if obj.touched > timezone.now()-timedelta(days=7):
            return "weekly"
        return "monthly"

    def priority(self, obj):
        posts_per_tag = obj.posts().count()
        total_posts = 100  # / Post.objects.all().count()
        priority = float(posts_per_tag) / float(total_posts)
        return priority

    def items(self):
        return Tag.objects.all()

    def lastmod(self, obj):
        return obj.touched
