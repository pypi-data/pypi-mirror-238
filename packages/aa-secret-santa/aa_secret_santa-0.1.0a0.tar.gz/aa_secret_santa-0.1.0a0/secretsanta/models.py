from discord import SyncWebhook
from solo.models import SingletonModel

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ("basic_access", "Can access Secret Santa"),
            ("manager", "Can Manage Secret Santa"),
        )


class Webhook(models.Model):
    name = models.CharField(
        _("Name"),
        max_length=100)
    url = models.URLField(
        _("URL"),
        max_length=200)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def send_embed(self, embed):
        webhook = SyncWebhook.from_url(self.url)
        webhook.send(embed=embed, username="Secret Santa")


class SecretSantaConfiguration(SingletonModel):
    delivery_updates = models.ManyToManyField(
        Webhook,
        verbose_name=_("Delivery Updates"),
        help_text=_("A Santee has marked they have received their gift")
    )

    def __str__(self):
        return "Secret Santa Configuration"

    class Meta:
        """
        Meta definitions
        """
        verbose_name = "Secret Santa Configuration"


class Year(models.Model):
    year = models.IntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2050)],
    )
    open = models.BooleanField(
        _("Open to Applications"),
        default=True,
    )

    @property
    def members(self) -> int:
        try:
            return Application.objects.filter(year=self).count()
        except Exception:
            return 0

    def get_users_santee(self, user: User) -> User:
        return SantaPair.objects.get(year=self, santa=user).santee


class Application(models.Model):
    """An Application to join Secret Santa"""
    year = models.ForeignKey(
        Year,
        verbose_name=_("Year"),
        on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE)

    class Meta:
        """
        Meta definitions
        """
        default_permissions = ()
        unique_together = ['year', 'user']


class SantaPair(models.Model):
    """A pairing of Santa's and Santee's"""
    year = models.ForeignKey(
        Year,
        verbose_name=_("Year"),
        on_delete=models.CASCADE)
    santa = models.ForeignKey(
        User,
        verbose_name=_("Santa"),
        on_delete=models.CASCADE,
        related_name="+")
    santee = models.ForeignKey(
        User,
        verbose_name=_("Santee"),
        on_delete=models.CASCADE,
        related_name="+")
    delivered = models.BooleanField(
        _("Delivered"),
        default=False)

    class Meta:
        """
        Meta definitions
        """
        default_permissions = ()
        unique_together = [['year', 'santa'], ['year', 'santee']]
