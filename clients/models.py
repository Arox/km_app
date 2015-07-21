# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
import datetime
from third_party.image_field import ResizedImageField
# Create your models here.
class LimitLikesQuerySet(models.QuerySet):
    LIMIT_LIKES = 10
    def update(self, **kwargs):
        return super(LimitLikesQuerySet, self.filter(likes__lt = self.LIMIT_LIKES)).update(**kwargs)

class Client(models.Model):
    name = models.CharField(_('name'), max_length=40, null=False)
    sername = models.CharField(_('sername'), max_length=60, null=False)
    birthday = models.DateField(_('birthday'), null=False, help_text=_('format: d.m.yyyy'))
    photo = ResizedImageField(max_width=200, max_height=300, format= 'JPEG', upload_to='photos/', max_length=20, null=True)

    likes = models.IntegerField(_('likes'), default=0, validators=[MaxValueValidator(LimitLikesQuerySet.LIMIT_LIKES), MinValueValidator(0)])
    objects = LimitLikesQuerySet.as_manager()

    @property
    def age(self):
        return int((datetime.date.today() - self.birthday).days // 365.25)

    class Meta:
        verbose_name = _('client')
        verbose_name_plural = _('clients')