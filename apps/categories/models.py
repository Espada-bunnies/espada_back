from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=32)
    logo = models.ImageField(upload_to='categories/logos', blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
