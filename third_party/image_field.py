# -*- coding: utf-8 -*-
'''
https://djangosnippets.org/snippets/1966/
example: image = ResizedImageField(upload_to='images/%Y/%m', blank=True, null=True)
'''
from PIL import Image

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.db.models.fields.files import ImageField, ImageFieldFile
from django.core.files.base import ContentFile


def _update_ext(filename, new_ext):
    parts = filename.split('.')
    parts[-1] = new_ext
    return '.'.join(parts)


class ResizedImageFieldFile(ImageFieldFile):

    def save(self, name, content, save=True):
        new_content = StringIO()
        content.file.seek(0)

        img = Image.open(content.file)
        width, height = img.size
        if width > self.field.max_width or height > self.field.max_height:
            print (width, height)
            kofs = (width / self.field.max_width, height / self.field.max_height)
            print (kofs)
            max_kof = max(kofs)
            width /= max_kof
            height /= max_kof
            print (width, height)

        img.thumbnail((
            width,
            height
            ), Image.ANTIALIAS)
        img.save(new_content, format=self.field.format)

        new_content = ContentFile(new_content.getvalue())
        new_name = _update_ext(name, self.field.format.lower())

        super(ResizedImageFieldFile, self).save(new_name, new_content, save)


class ResizedImageField(ImageField):

    attr_class = ResizedImageFieldFile

    def __init__(self, max_width=100, max_height=100, format='PNG', *args, **kwargs):
        self.max_width = max_width
        self.max_height = max_height
        self.format = format
        super(ResizedImageField, self).__init__(*args, **kwargs)