from django.db import models
from django.utils.translation import gettext_lazy as _


class ModerationStatusChoices(models.TextChoices):
    IN_MODERATION = "in_moderation", _("In moderation")
    ACTIVE = "active", _("Active")
    INACTIVE = "inactive", _("Inactive")
