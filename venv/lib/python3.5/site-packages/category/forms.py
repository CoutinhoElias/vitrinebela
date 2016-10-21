from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.layout import Fieldset
from crispy_forms.layout import ButtonHolder
from crispy_forms.layout import Submit
from crispy_forms.layout import Button
from crispy_forms.layout import Div


from .models import Category, Tag


class CategoryCreateForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'parent',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                'name',
                'parent',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-small'),
                Button('cancel', 'Cancel', css_class='btn-small')
            )
        )
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-inline'
        self.helper.form_action = 'planet:category-add'
        super(CategoryCreateForm, self).__init__(*args, **kwargs)


class CategoryUpdateForm(forms.ModelForm):
    """
    CategoryUpdateForm

    Django Form to modify an angryplanet-category

    ..author: Andreas Neumeier
    """
    class Meta:
        model = Category
        fields = ('name', 'slug', 'parent',)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Change Category',
                'name',
                'slug',
                'parent',
            ),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn-small'),
                Button('cancel', 'Cancel', css_class='btn-small')
            )
        )
        self.helper.form_method = 'post'
        super(CategoryUpdateForm, self).__init__(*args, **kwargs)


class TagCreateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name', )


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'parent',)
