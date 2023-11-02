from django.core.files import File

from product_images.models import ProductImage


def refresh_logo(instance):
    try:
        first_image = ProductImage.objects.filter(product=instance).first()

        if first_image:
            file = File(open(first_image.file.path, 'rb'))
            instance.logo.save(first_image.file.name, file)
        else:
            instance.logo.delete()
    except Exception as e:
        print(e)
