from django.contrib import admin
from django.utils.html import format_html
from parler.admin import TranslatableAdmin
from apps.market.models import (
	Category, TopLevelCategory, SubCategory, Product, ProductImage, ProductColor,
  	CommentAndReviewProduct
)


class ParentCategoryFilter(admin.SimpleListFilter):
	title = 'Родительская категория'
	parameter_name = 'parent'

	def lookups(self, request, model_admin):
		# Only show top-level categories as filter options
		top_level_categories = Category.objects.filter(parent__isnull=True)
		return [(cat.id, cat.safe_translation_getter('name', any_language=True) or 'Безымянный') for cat in top_level_categories]

	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(parent__id=self.value())
		return queryset


@admin.register(TopLevelCategory)
class TopLevelCategoryAdmin(TranslatableAdmin):
	list_display = ('translated_name', 'get_all_translations', 'created_at')
	search_fields = ('translations__name',)
	list_filter = ('created_at',)
	fieldsets = (
		('Основная информация', {
			'fields': ('name',),
			'description': 'Название категории на разных языках. Используйте вкладки языков выше для переключения между языками: RU | EN | UZ | KK | KO'
		}),
		('Дополнительная информация', {
			'fields': ('created_at',)
		}),
	)
	readonly_fields = ('created_at',)
	
	def get_all_translations(self, obj):
		"""Показать все переводы для быстрого просмотра"""
		translations = []
		for lang_code, lang_name in [('ru', 'RU'), ('en', 'EN'), ('uz', 'UZ'), ('kk', 'KK'), ('ko', 'KO')]:
			try:
				obj.set_current_language(lang_code)
				name = obj.name
				if name:
					translations.append(f"{lang_name}: {name}")
			except:
				pass
		return " | ".join(translations) if translations else "Нет переводов"
	
	get_all_translations.short_description = 'Переводы'

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		return qs.filter(parent__isnull=True)

	def translated_name(self, obj):
		return obj.safe_translation_getter('name', any_language=True) or 'Безымянный'

	translated_name.short_description = 'Название категория'

	def get_form(self, request, obj=None, **kwargs):
		form = super().get_form(request, obj, **kwargs)
		if obj is None or obj.parent is None:
			form.base_fields.pop('parent', None)
		return form
	
	class Media:
		css = {
			'all': ('parler/admin/parler_admin.css',)
		}


@admin.register(SubCategory)
class SubCategoryAdmin(TranslatableAdmin):
	list_display = ('translated_name', 'parent', 'get_all_translations', 'created_at')
	search_fields = ('translations__name', 'parent__translations__name')
	list_filter = (ParentCategoryFilter, 'created_at')
	fieldsets = (
		('Основная информация', {
			'fields': ('name', 'parent'),
			'description': 'Название подкатегории на разных языках. Используйте вкладки языков выше: RU | EN | UZ | KK | KO'
		}),
		('Дополнительная информация', {
			'fields': ('created_at',)
		}),
	)
	readonly_fields = ('created_at',)
	
	def get_all_translations(self, obj):
		"""Показать все переводы для быстрого просмотра"""
		translations = []
		for lang_code, lang_name in [('ru', 'RU'), ('en', 'EN'), ('uz', 'UZ'), ('kk', 'KK'), ('ko', 'KO')]:
			try:
				obj.set_current_language(lang_code)
				name = obj.name
				if name:
					translations.append(f"{lang_name}: {name}")
			except:
				pass
		return " | ".join(translations) if translations else "Нет переводов"
	
	get_all_translations.short_description = 'Переводы'

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		return qs.filter(parent__isnull=False, parent__parent__isnull=True)

	def translated_name(self, obj):
		return obj.safe_translation_getter('name', any_language=True) or 'Безымянный'

	translated_name.short_description = 'Название подкатегория'

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'parent':
			kwargs['queryset'] = Category.objects.filter(parent__isnull=True)
		return super().formfield_for_foreignkey(db_field, request, **kwargs)
	
	class Media:
		css = {
			'all': ('parler/admin/parler_admin.css',)
		}


class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 1
	fields = ('image', 'image_preview')
	readonly_fields = ('image_preview',)
	
	def image_preview(self, obj):
		if obj.image:
			return format_html(
				'<img src="{}" style="max-width: 200px; max-height: 200px; object-fit: cover; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />',
				obj.image.url
			)
		return "Нет изображения"
	
	image_preview.short_description = "Предварительный просмотр"
	
	def has_add_permission(self, request, obj=None):
		return True

	def has_delete_permission(self, request, obj=None):
		return True

	class Media:
		js = ('admin/js/image_preview.js',)
		css = {
			'all': ('admin/css/image_preview.css', 'parler/admin/parler_admin.css',)
		}


class ProductColorInline(admin.TabularInline):
	model = ProductColor
	extra = 1
	fields = ('color', 'color_preview')
	readonly_fields = ('color_preview',)

	def color_preview(self, obj):
		if obj.color:
			return format_html(
				'<div style="width: 30px; height: 30px; background-color: {}; border-radius: 4px; border: 1px solid #ccc;"></div>',
				obj.color
			)
		return "Нет цвета"

	color_preview.short_description = "Предварительный просмотр цвета"

	def has_add_permission(self, request, obj=None):
		return True

	def has_delete_permission(self, request, obj=None):
		return True


class CommentAndReviewProductInline(admin.TabularInline):
	model = CommentAndReviewProduct
	extra = 1
	fields = ('full_name', 'review_rating', 'content', 'created_at')
	readonly_fields = ('created_at',)

	def has_add_permission(self, request, obj=None):
		return True

	def has_delete_permission(self, request, obj=None):
		return True


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
	list_display = ('thumbnail_preview', 'translated_name', 'category', 'brand', 'price', 'discount_price', 'get_translation_status', 'created_at')
	search_fields = ('translations__name', 'category__translations__name', 'brand')
	list_filter = ('category', 'brand', 'created_at')
	fieldsets = (
		('Основная информация', {
			'fields': ('name', 'description', 'category', 'brand'),
			'description': 'Название и описание продукта переводится на все языки. Переключайтесь между языками: RU | EN | UZ | KK | KO'
		}),
		('Цены', {
			'fields': ('price', 'discount_price')
		}),
		('Изображения', {
			'fields': ('thumbnail', 'thumbnail_preview')
		}),
	)
	readonly_fields = ('thumbnail_preview',)
	inlines = [ProductImageInline, ProductColorInline, CommentAndReviewProductInline]
	
	def get_translation_status(self, obj):
		"""Показать статус переводов"""
		languages = [('ru', 'RU'), ('en', 'EN'), ('uz', 'UZ'), ('kk', 'KK'), ('ko', 'KO')]
		completed = []
		for lang_code, lang_name in languages:
			try:
				obj.set_current_language(lang_code)
				if obj.name:
					completed.append(lang_name)
			except:
				pass
		return f"{len(completed)}/5 ({', '.join(completed)})" if completed else "0/5"
	
	get_translation_status.short_description = 'Переводы'

	def translated_name(self, obj):
		return obj.safe_translation_getter('name', any_language=True) or 'Безымянный'
	translated_name.short_description = 'Название продукта'

	def thumbnail_preview(self, obj):
		if obj.thumbnail:
			return format_html(
				'<img src="{}" style="max-width: 100px; max-height: 100px; object-fit: cover; border-radius: 4px;" />',
				obj.thumbnail.url
			)
		return "Нет миниатюры"
	
	thumbnail_preview.short_description = "Миниатюра"

	def images_count(self, obj):
		return obj.images.count()
	images_count.short_description = 'Количество изображений'

	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == 'category':
			# Show only subcategories (categories that have a parent)
			kwargs['queryset'] = Category.objects.filter(parent__isnull=False).order_by('parent__id', 'id')
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

	def get_queryset(self, request):
		qs = super().get_queryset(request)
		return qs.prefetch_related('category__translations', 'images')

	class Media:
		js = ('admin/js/image_preview.js',)
		css = {
			'all': ('admin/css/image_preview.css',)
		}


