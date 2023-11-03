from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class SolarSystem(models.Model):
    id = models.PositiveIntegerField(_("Solar System ID"), primary_key=True)
    security_status = models.FloatField(
        _("Security Status"),
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])

    class Meta:
        verbose_name = _("Solar System")
        verbose_name_plural = _("Solar Systems")


class SolarSystemConnection(models.Model):
    fromsolarsystem = models.ForeignKey(
        SolarSystem,
        verbose_name=_("From Solar System"),
        on_delete=models.CASCADE,
        related_name="+")
    tosolarsystem = models.ForeignKey(
        SolarSystem,
        verbose_name=_("To Solar System"),
        on_delete=models.CASCADE,
        related_name="+")

    prefer_shortest = models.FloatField(_("Weighting for Prefer Shortest Routing"), default=1)
    prefer_safest = models.FloatField(_("Weighting for Prefer Safest Routing"), default=1)
    prefer_less_safe = models.FloatField(_("Weighting for Prefer Less Safe Routing"), default=1)

    class Meta:
        verbose_name = _("Solar System Connections")
        verbose_name_plural = _("Solar System Connection")
        unique_together = ["fromsolarsystem", "tosolarsystem"]


class TrigInvasion(models.Model):

    class Status(models.TextChoices):
        """"
        The system status after the Triglavian Invasion
        """
        EDENCOM_MINOR_VICTORY = 'edencom_minor_victory', _("EDENCOM Minor Victory")
        FINAL_LIMINALITY = 'final_liminality', _("Final Liminality")
        FORTRESS = 'fortress', _("Fortress")
        TRIGLAVIAN_MINOR_VICTORY = 'triglavian_minor_victory', _("Triglavian Minor Victory")

    system = models.OneToOneField(
        SolarSystem,
        verbose_name=_("Solar System"),
        on_delete=models.CASCADE,
        related_name="+",
        primary_key=True)

    status = models.CharField(_("Mass Remaining"), max_length=50, choices=Status.choices)

    class Meta:
        verbose_name = _("Triglavian/Edencom Invasion")
        verbose_name_plural = _("Triglavian/Edencom Invasions")
