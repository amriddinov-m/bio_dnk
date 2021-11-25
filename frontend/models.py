from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1, defaults={'title': '-'})
        return obj


class Chain(SingletonModel):
    title = models.TextField(max_length=255,
                             blank=True, null=True,
                             verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Цепочка'
        verbose_name_plural = 'Цепочки'
