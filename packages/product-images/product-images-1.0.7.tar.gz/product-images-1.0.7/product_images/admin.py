from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from product_images.fields import ImagesFormField


class ImagesForm(forms.ModelForm):

    images = ImagesFormField(label='')

    def __init__(self, *args, **kwargs):

        super(ImagesForm, self).__init__(*args, **kwargs)

        self.fields['images'].init_form(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=commit)

        if commit:
            self.fields['images'].commit(instance)

        return instance


def get_logo_cell(product):
    images = list(product.images.all())
    return mark_safe(
        render_to_string("product-admin-preview.html", {
            "product": product,
            "images": images
        })
    )
