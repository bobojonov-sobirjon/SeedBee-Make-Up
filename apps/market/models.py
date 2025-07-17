from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from parler.managers import TranslatableManager
from parler.models import TranslatableModel, TranslatedFields
from colorfield.fields import ColorField

User = get_user_model()


class Category(TranslatableModel):
    translations = TranslatedFields(name=models.CharField(_("Категория Имя"), max_length=250, null=True, blank=True))
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories', verbose_name=_("Категория Родитель"))
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name=_("Дата создания"))
    objects = TranslatableManager()

    def __str__(self):
        str_name = self.safe_translation_getter('name', any_language=True) or "Без названия"
        parent = self.parent
        while parent:
            parent_name = parent.safe_translation_getter('name', any_language=True) or "Без названия"
            str_name = f'{parent_name} / {str_name}'
            parent = parent.parent
        return str_name

    class Meta:
        ordering = ["id"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class TopLevelCategory(Category):
    class Meta:
        proxy = True
        verbose_name = _("Основная категория")
        verbose_name_plural = _("1. Основные категории")


class SubCategory(Category):
    class Meta:
        proxy = True
        verbose_name = _("Подкатегория")
        verbose_name_plural = _("2. Подкатегории")


class Product(TranslatableModel):
    translations = TranslatedFields(
        name=models.CharField(_("Название продукта"), max_length=250, null=True, blank=True),
        description=models.TextField(_("Описание продукта"), null=True, blank=True)
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name=_("Категория продукта"), null=True, blank=True)
    price = models.FloatField(_("Цена"), default=0.0, null=True, blank=True)
    discount_price = models.FloatField(_("Цена со скидкой"), default=0.0, null=True, blank=True)
    thumbnail = models.ImageField(_("Миниатюра продукта"), upload_to='products/thumbnails/', null=True, blank=True)
    brand = models.CharField(_("Бренд"), max_length=100, null=True, blank=True)
    is_popular = models.BooleanField(_("Популярный продукт"), default=False, null=True, blank=True)
    is_new = models.BooleanField(_("Новый продукт"), default=False, null=True, blank=True)
    is_discounted = models.BooleanField(_("Продукт со скидкой"), default=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or "Без названия"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Продукт")
        verbose_name_plural = _("3. Продукты")


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name=_("Изображение продукта"), null=True, blank=True)
    image = models.ImageField(_("Изображение"), upload_to='products/images/')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    def __str__(self):
        product_name = self.product.safe_translation_getter('name', any_language=True) if self.product else "Без названия"
        return f"Image for {product_name}"

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("Изображение продукта")
        verbose_name_plural = _("Изображения продуктов")


class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors', verbose_name=_("Цвет продукта"), null=True, blank=True)
    color = ColorField(format="hexa", verbose_name=_("Цвет"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    def __str__(self):
        return f"Color {self.color} for {self.product.safe_translation_getter('name', any_language=True) if self.product else 'Без названия'}"

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("Цвет продукта")
        verbose_name_plural = _("Цвета продуктов")


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name=_("Пользователь"))
    total_price = models.FloatField(_("Общая цена"), default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    def __str__(self):
        return f"Order #{self.id} by {self.user.email if self.user else 'Unknown User', self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Заказ")
        verbose_name_plural = _("4. Заказы")


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products', verbose_name=_("Заказ"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products', verbose_name=_("Продукт"))
    quantity = models.PositiveIntegerField(_("Количество"), default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.safe_translation_getter('name', any_language=True) if self.product else 'Без названия'} in Order #{self.order.id}"

    class Meta:
        ordering = ["order", "product"]
        verbose_name = _("Продукт заказа")
        verbose_name_plural = _("Продукты заказов")


class CommentAndReviewProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Комментарий продукта"))
    full_name = models.CharField(_("Полное имя пользователя"), max_length=100, null=True, blank=True)
    content = models.TextField(_("Содержание комментария"), null=True, blank=True)
    review_rating = models.PositiveIntegerField(_("Рейтинг отзыва"), default=0, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    def __str__(self):
        return f"Comment by {self.full_name if self.full_name else 'Unknown User'} on {self.product.safe_translation_getter('name', any_language=True) if self.product else 'Без названия'}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Комментарий и отзывы продукта")
        verbose_name_plural = _("Комментарии и отзывы продуктов")


        