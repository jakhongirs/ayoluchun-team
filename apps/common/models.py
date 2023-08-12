from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True


class Country(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    code = models.CharField(max_length=2, verbose_name=_("Code"))
    is_active = models.BooleanField(verbose_name=_("Is active"), default=True)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.name


class Region(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    soato = models.CharField(max_length=255, verbose_name=_("Soato"), unique=True)
    country = models.ForeignKey(
        Country,
        related_name="regions",
        on_delete=models.CASCADE,
        verbose_name=_("Country"),
    )
    is_active = models.BooleanField(verbose_name=_("Is active"), default=True)

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return self.name
