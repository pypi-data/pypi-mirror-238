import uuid

from PIL import Image

from os.path import basename
from urllib.request import urlretrieve

from django.db import models
from django.urls import reverse
from django.core.files import File
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from imagekit.processors import ResizeToFit
from imagekit.models import ProcessedImageField

from sorl.thumbnail import get_thumbnail


class ProductImage(models.Model):

    product = models.ForeignKey(
        'products.Product',
        verbose_name=_("Product"),
        related_name='images',
        on_delete=models.CASCADE,
        null=True,
        blank=True)

    file = models.ImageField(
        verbose_name=_("File"),
        upload_to='product_images',
        max_length=255)

    order = models.PositiveIntegerField(_('Ordering'))

    def __str__(self):
        return str(self.product)

    def get_preview_url(self):
        try:
            return get_thumbnail(self.file.file, '100').url
        except IOError:
            pass

        return ''

    def get_remove_url(self):
        return reverse('product-images:remove', args=[self.pk])

    @classmethod
    def create_from_url(cls, url):

        result = urlretrieve(url)

        return cls.objects.create(
            file=File(open(result[0], 'rb'), name=basename(url)))

    def compress(self):

        max_size = 2000, 2000

        try:
            img = Image.open(self.file.path)
            img.thumbnail(max_size, Image.ANTIALIAS)
            img.save(self.file.path, quality=70)
        except Exception as e:
            print(e)

    class Meta:
        db_table = 'products_productimage'
        ordering = ['order']
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


def random_filename(instance, filename):
    random_name = str(uuid.uuid4())
    ext = filename.split('.')[-1]
    return f'product_thumbnails/{random_name}.{ext}'


class LogoField(ProcessedImageField):

    def __init__(
            self,
            verbose_name=_('Logo'),
            upload_to=random_filename,
            blank=True,
            null=True,
            max_length=255,
            editable=False,
            width=260,
            height=200,
            format='WEBP',
            quality=60,
            *args, **kwargs):

        super(LogoField, self).__init__(
            verbose_name=verbose_name,
            upload_to=upload_to,
            blank=blank,
            null=null,
            max_length=max_length,
            editable=editable,
            processors=[ResizeToFit(width, height)],
            format=format,
            options={'quality': quality},
            *args, **kwargs)


def _post_process_image(sender, instance, created, **kwargs):

    if not created:
        return

    instance.compress()

    try:
        from watermarks.utils import insert_watermark
        insert_watermark('product', instance.file.path)
    except Exception as e:
        pass


post_save.connect(_post_process_image, sender=ProductImage)
