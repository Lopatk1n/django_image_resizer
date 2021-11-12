from django.db import models


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, verbose_name='Название', blank=True)
    url = models.CharField(max_length=250, verbose_name='Адрес', blank=True, null=True)
    picture = models.ImageField(upload_to='images/', verbose_name='Место хранения файла', blank=True, default='')
    width = models.IntegerField(verbose_name='Ширина')
    height = models.IntegerField(verbose_name='Высота')
    parent_picture = models.IntegerField(verbose_name='id оригинала', blank=True, null=True)
