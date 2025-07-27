from django.contrib import admin
from django.utils.html import format_html
from parler.admin import TranslatableAdmin

from apps.banner.models import (
	Banner, Partner, Advertisement, Blog
)


@admin.register(Banner)
class BannerAdmin(TranslatableAdmin):
	list_display = ('image_preview', 'russian_title', 'get_translation_status', 'created_at')
	search_fields = ('translations__title',)
	list_filter = ('created_at',)
	fieldsets = (
		('Основная информация', {
			'fields': ('title', 'description'),
			'description': 'Заголовок и описание баннера на разных языках. Используйте вкладки языков выше: RU | EN | UZ | KK | KO'
		}),
		('Изображение', {
			'fields': ('image', 'image_preview')
		}),
		('Дополнительная информация', {
			'fields': ('link', 'created_at')
		}),
	)
	readonly_fields = ('image_preview', 'created_at')

	def russian_title(self, obj):
		"""Return Russian translation of the title"""
		try:
			obj.set_current_language('ru')
			return obj.title or 'Без названия'
		except:
			return obj.safe_translation_getter('title', any_language=True) or 'Без названия'
	
	russian_title.short_description = 'Название (RU)'

	def get_translation_status(self, obj):
		"""Показать статус переводов"""
		languages = [('ru', 'RU'), ('en', 'EN'), ('uz', 'UZ'), ('kk', 'KK'), ('ko', 'KO')]
		completed = []
		for lang_code, lang_name in languages:
			try:
				obj.set_current_language(lang_code)
				title = obj.title
				if title and title.strip():  # Check if title exists and is not empty/whitespace
					completed.append(lang_name)
			except:
				pass
		return f"{len(completed)}/5 ({', '.join(completed)})" if completed else "0/5"
	
	get_translation_status.short_description = 'Переводы'

	def image_preview(self, obj):
		if obj.image:
			return format_html(
				'<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
				obj.image.url
			)
		return "Нет изображения"
	
	image_preview.short_description = "Предварительный просмотр"

	class Media:
		js = ('admin/js/image_preview.js',)
		css = {
			'all': ('admin/css/image_preview.css', 'parler/admin/parler_admin.css',)
		}


@admin.register(Partner)
class PartnerAdmin(TranslatableAdmin):
	list_display = ('image_preview', 'russian_title', 'get_translation_status', 'created_at')
	search_fields = ('translations__title',)
	list_filter = ('created_at',)
	fieldsets = (
		('Основная информация', {
			'fields': ('title', 'description'),
			'description': 'Заголовок и описание партнера на разных языках. Используйте вкладки языков выше: RU | EN | UZ | KK | KO'
		}),
		('Изображение', {
			'fields': ('image', 'image_preview')
		}),
		('Дополнительная информация', {
			'fields': ('link', 'created_at')
		}),
	)
	readonly_fields = ('image_preview', 'created_at')

	def russian_title(self, obj):
		"""Return Russian translation of the title"""
		try:
			obj.set_current_language('ru')
			return obj.title or 'Без названия'
		except:
			return obj.safe_translation_getter('title', any_language=True) or 'Без названия'
	
	russian_title.short_description = 'Название (RU)'

	def get_translation_status(self, obj):
		"""Показать статус переводов"""
		languages = [('ru', 'RU'), ('en', 'EN'), ('uz', 'UZ'), ('kk', 'KK'), ('ko', 'KO')]
		completed = []
		for lang_code, lang_name in languages:
			try:
				obj.set_current_language(lang_code)
				title = obj.title
				if title and title.strip():  # Check if title exists and is not empty/whitespace
					completed.append(lang_name)
			except:
				pass
		return f"{len(completed)}/5 ({', '.join(completed)})" if completed else "0/5"
	
	get_translation_status.short_description = 'Переводы'

	def image_preview(self, obj):
		if obj.image:
			return format_html(
				'<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
				obj.image.url
			)
		return "Нет изображения"
	
	image_preview.short_description = "Предварительный просмотр"

	class Media:
		js = ('admin/js/image_preview.js',)
		css = {
			'all': ('admin/css/image_preview.css', 'parler/admin/parler_admin.css',)
		}


@admin.register(Advertisement)
class AdvertisementAdmin(TranslatableAdmin):
	list_display = ('image_preview', 'russian_title', 'get_translation_status', 'created_at')
	search_fields = ('translations__title',)
	list_filter = ('created_at',)
	fieldsets = (
		('Основная информация', {
			'fields': ('title', 'description'),
			'description': 'Заголовок и описание рекламы на разных языках. Используйте вкладки языков выше: RU | EN | UZ | KK | KO'
		}),
		('Изображение', {
			'fields': ('image', 'image_preview')
		}),
		('Дополнительная информация', {
			'fields': ('link', 'created_at')
		}),
	)
	readonly_fields = ('image_preview', 'created_at')

	def russian_title(self, obj):
		"""Return Russian translation of the title"""
		try:
			obj.set_current_language('ru')
			return obj.title or 'Без названия'
		except:
			return obj.safe_translation_getter('title', any_language=True) or 'Без названия'
	
	russian_title.short_description = 'Название (RU)'

	def get_translation_status(self, obj):
		"""Показать статус переводов"""
		languages = [('ru', 'RU'), ('en', 'EN'), ('uz', 'UZ'), ('kk', 'KK'), ('ko', 'KO')]
		completed = []
		for lang_code, lang_name in languages:
			try:
				obj.set_current_language(lang_code)
				title = obj.title
				if title and title.strip():  # Check if title exists and is not empty/whitespace
					completed.append(lang_name)
			except:
				pass
		return f"{len(completed)}/5 ({', '.join(completed)})" if completed else "0/5"
	
	get_translation_status.short_description = 'Переводы'

	def image_preview(self, obj):
		if obj.image:
			return format_html(
				'<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
				obj.image.url
			)
		return "Нет изображения"
	
	image_preview.short_description = "Предварительный просмотр"

	class Media:
		js = ('admin/js/image_preview.js',)
		css = {
			'all': ('admin/css/image_preview.css', 'parler/admin/parler_admin.css',)
		}


@admin.register(Blog)
class BlogAdmin(TranslatableAdmin):
	list_display = ('image_preview', 'russian_title', 'get_translation_status', 'created_at')
	search_fields = ('translations__title',)
	list_filter = ('created_at',)
	fieldsets = (
		('Основная информация', {
			'fields': ('title', 'content'),
			'description': 'Заголовок и содержание блога на разных языках. Используйте вкладки языков выше: RU | EN | UZ | KK | KO'
		}),
		('Изображение', {
			'fields': ('image', 'image_preview')
		}),
		('Дополнительная информация', {
			'fields': ('link', 'created_at')
		}),
	)
	readonly_fields = ('image_preview', 'created_at')

	def russian_title(self, obj):
		"""Return Russian translation of the title"""
		try:
			obj.set_current_language('ru')
			return obj.title or 'Без названия'
		except:
			return obj.safe_translation_getter('title', any_language=True) or 'Без названия'
	
	russian_title.short_description = 'Название (RU)'

	def get_translation_status(self, obj):
		"""Показать статус переводов"""
		languages = [('ru', 'RU'), ('en', 'EN'), ('uz', 'UZ'), ('kk', 'KK'), ('ko', 'KO')]
		completed = []
		for lang_code, lang_name in languages:
			try:
				obj.set_current_language(lang_code)
				title = obj.title
				if title and title.strip():  # Check if title exists and is not empty/whitespace
					completed.append(lang_name)
			except:
				pass
		return f"{len(completed)}/5 ({', '.join(completed)})" if completed else "0/5"
	
	get_translation_status.short_description = 'Переводы'

	def image_preview(self, obj):
		if obj.image:
			return format_html(
				'<img src="{}" style="max-width: 150px; max-height: 150px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
				obj.image.url
			)
		return "Нет изображения"
	
	image_preview.short_description = "Предварительный просмотр"

	class Media:
		js = ('admin/js/image_preview.js',)
		css = {
			'all': ('admin/css/image_preview.css', 'parler/admin/parler_admin.css',)
		}

