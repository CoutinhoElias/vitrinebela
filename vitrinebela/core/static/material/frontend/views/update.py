from django.core.urlresolvers import reverse
from django.views import generic

from .mixins import MessageUserMixin, ModelViewMixin


class UpdateModelView(MessageUserMixin, ModelViewMixin, generic.UpdateView):
    """Thin `generic.UpdateView` wrapper plays nice with `ModelViewSet`."""

    template_name_suffix = '_update'

    def has_object_permission(self, request, obj):
        """Object change permission check.

        If view had a `viewset`, the `viewset.has_change_permission` used.
        """
        if self.viewset is not None:
            return self.viewset.has_change_permission(request, obj)
        raise NotImplementedError('Viewset is not provided')

    def get_success_url(self):
        """Redirect back to the detail view if no `success_url` is configured."""
        if self.success_url is None:
            opts = self.model._meta
            return reverse('{}:{}_detail'.format(
                opts.app_label, opts.model_name), args=[self.object.pk]
            )
        return super(ModelViewMixin, self).get_success_url()

    def message_user(self):
        self.success('The {name} "{link}" was changed successfully.')
