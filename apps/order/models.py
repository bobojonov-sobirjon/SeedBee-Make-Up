from django.db import models
from apps.accounts.models import CustomUser
from apps.market.models import Product
from django.utils.translation import gettext_lazy as _
import uuid


class CardDetails(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='card_details', verbose_name=_("Пользователь"))
    card_number = models.CharField(max_length=16, verbose_name=_("Номер карты"))
    card_holder = models.CharField(max_length=255, verbose_name=_("Имя держателя карты"))
    expiration_date = models.CharField(max_length=4, verbose_name=_("Дата истечения (MMYY)"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    payme_token = models.TextField(null=True, blank=True, verbose_name=_("Payme Token"))
    verified = models.BooleanField(default=False, verbose_name=_("Verified"))
    
    objects = models.Manager()
    
    def __str__(self):
        return f"Card #{self.id} by {self.user.email if self.user else 'Unknown User'}, {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    @property
    def masked_card_number(self):
        return f"**** **** **** {self.card_number[-4:]}";  # Mask all but last 4 digits
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Детали карты")
        verbose_name_plural = _("Детали карт")


class Order(models.Model):
    PAYMENT_STATES = (
        (0, "Чек создан. Ожидание подтверждения оплаты."),
        (1, "Первая стадия проверок. Создание транзакции в биллинге поставщика."),
        (2, "Списание денег с карты"),
        (3, "Закрытие транзакции в биллинге поставщика"),
        (4, "Чек оплачен"),
        (5, "Чек заходирован"),
        (6, "Получение команды на холдирование средств. Если чек находится в этом статусе достаточно долго - необходимо обратиться к техническим специалистам Payme Business"),
        (20, "Чек стоит на паузе для ручного вмешательства"),
        (21, "Чек в очереди на отмену"),
        (30, "Чек в очереди на закрытие транзакции в биллинге поставщика"),
        (50, "Чек отменен"),
    )
    order_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name=_("ID заказа"))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', verbose_name=_("Пользователь"))
    products = models.JSONField(verbose_name=_("Продукты"), null=True, blank=True)
    total_price = models.FloatField(_("Общая цена"), default=0.0)
    payment_status = models.IntegerField(_("Статус оплаты"), choices=PAYMENT_STATES, default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    
    objects = models.Manager()
    
    def __str__(self):
        return f"Order #{self.id} by {self.user.email if self.user else 'Unknown User'}, {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Заказ")
        verbose_name_plural = _("Заказы")
        