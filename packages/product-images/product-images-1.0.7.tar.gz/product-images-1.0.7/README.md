### Installation
* Add `product_images` to `INSTALLED_APPS`
* Add `product-images` to requirements
* Extend `ProductForm` from `product_images.admin.ImagesForm`
* Add `logo = LogoField()` to `Product` model.

Admin preview example:
```
from product_images.admin import get_logo_cell


@admin.display(description=_("Preview"))
def get_preview(self, obj):
    return get_logo_cell(obj)
    
def get_queryset(self, request):
    queryset = super().get_queryset(request)
    queryset = queryset.prefetch_related('images')
    return queryset

def save_model(self, request, obj, form, change):
    form.save()
```
