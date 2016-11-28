from django.views import generic

from .mixins import MessageUserMixin, ModelViewMixin


class CreateModelView(MessageUserMixin, ModelViewMixin, generic.CreateView):
    """Thin `generic.CreateView` wrapper plays nice with `ModelViewSet`."""

    template_name_suffix = '_create'

    def has_object_permission(self, request, obj):
        """Object add permission check.

        If view had a `viewset`, the `viewset.has_add_permission` used.
        """
        if self.viewset is not None:
            return self.viewset.has_add_permission(request, obj)
        raise NotImplementedError('Viewset is not provided')

    def message_user(self):
        self.success('The {name} "{link}" was added successfully.')
