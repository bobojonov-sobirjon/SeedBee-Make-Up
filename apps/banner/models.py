from django.db import models
from parler.managers import TranslatableManager
from parler.models import TranslatableModel, TranslatedFields


class Banner(TranslatableModel):
	translations = TranslatedFields(
		title=models.CharField("Заголовок баннера", max_length=250, null=True, blank=True),
		description=models.TextField("Описание баннера", null=True, blank=True)
	)
	image = models.ImageField("Изображение баннера", upload_to='banners/', null=True, blank=True)
	link = models.URLField("Ссылка на баннер", max_length=500, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

	objects = TranslatableManager()

	def __str__(self):
		return self.safe_translation_getter('title', any_language=True) or "Без заголовка"

	class Meta:
		verbose_name = "Баннер"
		verbose_name_plural = "1. Баннеры"


class Partner(TranslatableModel):
	translations = TranslatedFields(
		title=models.CharField("Заголовок баннера", max_length=250, null=True, blank=True),
		description=models.TextField("Описание баннера", null=True, blank=True)
	)
	image = models.ImageField("Изображение баннера", upload_to='banners/', null=True, blank=True)
	link = models.URLField("Ссылка на баннер", max_length=500, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

	objects = TranslatableManager()

	def __str__(self):
		return self.safe_translation_getter('title', any_language=True) or "Без заголовка"

	class Meta:
		verbose_name = "Партнер"
		verbose_name_plural = "2. Партнеры"


class Advertisement(TranslatableModel):
	translations = TranslatedFields(
		title=models.CharField("Заголовок рекламы", max_length=250, null=True, blank=True),
		description=models.TextField("Описание рекламы", null=True, blank=True)
	)
	image = models.ImageField("Изображение рекламы", upload_to='advertisements/', null=True, blank=True)
	link = models.URLField("Ссылка на рекламу", max_length=500, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

	objects = TranslatableManager()

	def __str__(self):
		return self.safe_translation_getter('title', any_language=True) or "Без заголовка"

	class Meta:
		verbose_name = "Реклама"
		verbose_name_plural = "3. Реклама"


class Blog(TranslatableModel):
	translations = TranslatedFields(
		title=models.CharField("Заголовок блога", max_length=250, null=True, blank=True),
		content=models.TextField("Содержание блога", null=True, blank=True)
	)
	image = models.ImageField("Изображение блога", upload_to='blogs/', null=True, blank=True)
	link = models.URLField("Ссылка на блог", max_length=500, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

	objects = TranslatableManager()

	def __str__(self):
		return self.safe_translation_getter('title', any_language=True) or "Без заголовка"

	class Meta:
		verbose_name = "Блог"
		verbose_name_plural = "4. Блоги"