from django.db import models
from apps.accounts.models import CustomUser
from apps.market.models import Product
from django.utils.translation import gettext_lazy as _



# class OrderProduct(models.Model):
#     products = models.JSONField(verbose_name=_("Продукты"), null=True, blank=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='order_products', verbose_name=_("Пользователь"))
#     total_price = models.FloatField(_("Общая цена"), default=0.0)
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    
#     objects = models.Manager()
    
#     def __str__(self):
#         return f"Order #{self.id} by {self.user.email if self.user else 'Unknown User'}, {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
#     class Meta:
#         ordering = ["-created_at"]
#         verbose_name = _("Продукты заказа")
#         verbose_name_plural = _("Продукты заказов")