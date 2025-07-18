from django.db import models
from apps.accounts.models import CustomUser
from apps.market.models import Product
from django.utils.translation import gettext_lazy as _
import uuid


class CardDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='card_details', verbose_name=_("Пользователь"))
    card_number = models.CharField(max_length=16, verbose_name=_("Номер карты"))
    card_holder = models.CharField(max_length=255, verbose_name=_("Имя держателя карты"))
    expiration_date = models.DateField(verbose_name=_("Дата истечения срока действия"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    
    objects = models.Manager()
    
    def __str__(self):
        return f"Card #{self.id} by {self.user.email if self.user else 'Unknown User'}, {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Детали карты")
        verbose_name_plural = _("Детали карт")


class Order(models.Model):
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name=_("ID заказа"))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', verbose_name=_("Пользователь"))
    products = models.JSONField(verbose_name=_("Продукты"), null=True, blank=True)
    total_price = models.FloatField(_("Общая цена"), default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    
    objects = models.Manager()
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.email if self.user else 'Unknown User'}, {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")
        