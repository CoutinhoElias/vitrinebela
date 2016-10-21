from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class TagManager(models.Manager):
    """
    Manager for `Tag` objects.
    """

    def get_by_natural_key(self, slug):
        """
        get Tag by natural key, to allow serialization by key rather than `pk`
        """
        return self.get(slug=slug)


@python_2_unicode_compatible
class Tag(models.Model):
    """
    A tag.
    """

    objects = TagManager()
    """
    Overwrite the inherited manager with the
    custom :mod:`feeds.models.TagManager`
    """

    name = models.CharField(
        _('name'),
        max_length=50,
        unique=True,
        db_index=True
    )
    """The name of the Tag."""

    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        help_text='Short descriptive unique name for use in urls.',
    )
    """
    The slug of the Tag.
    It can be used in any URL referencing this particular Tag.
    """

    relevant = models.BooleanField(default=False)
    """
    Indicates whether this Tag is relevant for further processing.
    It should be used to allow administrative intervention.
    """

    touched = models.DateTimeField(auto_now=True)
    """Keep track of when this Tag was last used."""

    content_type = models.ForeignKey(
        ContentType,
        null=True,
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    @classmethod
    def create(cls, name, slug=None):
        tag = cls(name=name)
        if not slug:
            tag.slug = slugify(tag.name)
        tag.save()
        print("Tag name, slug: %s, %s" % (tag.name, tag.slug))
        return tag

    class Meta:
        """
        Django Meta.
        """
        ordering = ('name',)
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        """
        Human readable representation of the object.
        """
        return u''.join(self.name)

    def natural_key(self):
        return u''.join(self.slug)

    @models.permalink
    def get_absolute_url(self):
        return ('category:tag-view', [str(self.slug)])


class CategoryManager(models.Manager):
    """
    Manager for Category
    """
    def get_by_natural_key(self, slug):
        """
        Get Category by natural kea to allow serialization
        """
        return self.get(slug=slug)


@python_2_unicode_compatible
class Category(models.Model):
    """
    Category model to be used for categorization of content. Categories are
    high level constructs to be used for grouping and organizing content,
    thus creating a site's table of contents.
    """
    objects = CategoryManager()

    name = models.CharField(
        max_length=200,
        help_text='Short descriptive name for this category.',
    )

    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        help_text='Short descriptive unique name for use in urls.',
    )

    parent = models.ForeignKey('self', null=True, blank=True)

    @classmethod
    def create(cls, name, slug=None):
        cat = cls(name=name)
        if not slug:
            cat.slug = slugify(cat.name)
        cat.save()
        print("Category name, slug: %s, %s" % (cat.name, cat.slug))
        return cat

    class Meta:
        """
        Django Meta.
        """
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    @property
    def children(self):
        return self.category_set.all().order_by('name')

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "":
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        """
        Human readable representation of the object.
        """
        return u''.join(self.name)

    def natural_key(self):
        return u''.join(self.slug)

    @models.permalink
    def get_absolute_url(self):
        return ('category:category-view', [str(self.slug)])
