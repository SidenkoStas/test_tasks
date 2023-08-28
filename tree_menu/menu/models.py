from django.db import models
from django.urls import reverse


class Menu(models.Model):
    """
    Название отдельных меню.
    """
    title = models.CharField(max_length=150, verbose_name="Название меню")
    slug = models.SlugField(db_index=True, unique=True)

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return f"{self.title}"


class Section(models.Model):
    """
    Древовидное меню построенное методом 'Adjacency list'
    """
    title = models.CharField(max_length=150, verbose_name="Название раздела")
    slug = models.SlugField(db_index=True, unique=True, verbose_name="slug")
    menu = models.ForeignKey("Menu", on_delete=models.PROTECT,
                             related_name="tree", verbose_name="Меню")
    parent = models.ForeignKey("self", on_delete=models.PROTECT, blank=True,
                               null=True, related_name="child",
                               verbose_name="Родитель")

    class Meta:
        verbose_name = "Раздел"
        verbose_name_plural = "Разделы"

    def get_absolute_url(self):
        return reverse("menu:section", kwargs={"name": self.menu,
                                               "section_pk": self.pk})

    def __str__(self):
        return f"{self.title}"
