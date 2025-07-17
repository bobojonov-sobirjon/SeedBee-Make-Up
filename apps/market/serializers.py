from rest_framework import serializers

from apps.market.models import (
	TopLevelCategory, SubCategory, Category, Product, ProductImage, ProductColor,
	Order, OrderProduct, CommentAndReviewProduct
)


class SubCategorySerializer(serializers.ModelSerializer):
	translated_name = serializers.SerializerMethodField()
	parent = serializers.SerializerMethodField()

	class Meta:
		model = SubCategory
		fields = ['id', 'translated_name', 'parent', 'created_at']
		read_only_fields = ['created_at']

	def get_parent(self, obj):
		return obj.parent.name

	def get_translated_name(self, obj):
		"""Get all translations for all languages"""
		translations = {}
		for lang_code, lang_name in [('ru', 'russian'), ('en', 'english'), ('uz', 'uzbek'), ('kk', 'kazakh'), ('ko', 'korean')]:
			try:
				obj.set_current_language(lang_code)
				name = obj.name
				if name:
					translations[lang_code] = name
			except:
				pass
		try:
			obj.set_current_language('ru')
		except:
			pass
		return translations


class TopLevelCategorySerializer(serializers.ModelSerializer):
	sub_categories = serializers.SerializerMethodField()
	translated_name = serializers.SerializerMethodField()

	class Meta:
		model = TopLevelCategory
		fields = ['id', 'translated_name', 'sub_categories', 'created_at']
		read_only_fields = ['created_at']

	def get_sub_categories(self, obj):
		sub_categories = obj.subcategories.all()
		return SubCategorySerializer(sub_categories, many=True, context=self.context).data

	def get_translated_name(self, obj):
		"""Get all translations for all languages"""
		translations = {}
		for lang_code, lang_name in [('ru', 'russian'), ('en', 'english'), ('uz', 'uzbek'), ('kk', 'kazakh'), ('ko', 'korean')]:
			try:
				obj.set_current_language(lang_code)
				name = obj.name
				if name:
					translations[lang_code] = name
			except:
				pass
		try:
			obj.set_current_language('ru')
		except:
			pass
		return translations


class ProductImageSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductImage
		fields = ['id', 'image']


class ProductColorSerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductColor
		fields = ['id', 'color']


class CommentAndReviewProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommentAndReviewProduct
		fields = ['id', 'full_name', 'content', 'review_rating', 'created_at']
		read_only_fields = ['created_at']


class ProductSerializer(serializers.ModelSerializer):
	images = ProductImageSerializer(many=True, read_only=True)
	colors = ProductColorSerializer(many=True, read_only=True)
	translated_name = serializers.SerializerMethodField()
	translated_description = serializers.SerializerMethodField()
	comment_count = serializers.SerializerMethodField()
	total_rating = serializers.SerializerMethodField()
	comment_and_review = serializers.SerializerMethodField()
	category = serializers.SerializerMethodField()
	is_news = serializers.SerializerMethodField()
	is_populars = serializers.SerializerMethodField()

	class Meta:
		model = Product
		fields = ['id', 'translated_name', 'translated_description', 'category', 'price', 'discount_price', 'thumbnail', 'brand', 'images', 'colors',
				  'comment_count', 'comment_and_review', 'total_rating', 'is_news', 'is_populars', 'is_new', 'is_popular', 'is_discounted', 'created_at']
		read_only_fields = ['created_at']

	def get_is_news(self, obj):
		from datetime import timedelta
		from django.utils import timezone
		now = timezone.now()
		return (now - obj.created_at) <= timedelta(days=3)

	def get_is_populars(self, obj):
		if obj.comments.exists():
			total_rating = sum(comment.review_rating for comment in obj.comments.all())
			avg_rating = total_rating / obj.comments.count()
			return avg_rating > 4.5
		return False

	def get_category(self, obj):
		"""Get the category name for the product."""
		if obj.category:
			serializers = SubCategorySerializer(obj.category, context=self.context)
			return serializers.data
		return "Нет категории"

	def get_translated_name(self, obj):
		"""Get all translations for all languages"""
		translations = {}
		for lang_code, lang_name in [('ru', 'russian'), ('en', 'english'), ('uz', 'uzbek'), ('kk', 'kazakh'), ('ko', 'korean')]:
			try:
				obj.set_current_language(lang_code)
				name = obj.name
				if name:
					translations[lang_code] = name
			except:
				pass
		try:
			obj.set_current_language('ru')
		except:
			pass
		return translations

	def get_translated_description(self, obj):
		"""Get all translations for all languages"""
		translations = {}
		for lang_code, lang_name in [('ru', 'russian'), ('en', 'english'), ('uz', 'uzbek'), ('kk', 'kazakh'), ('ko', 'korean')]:
			try:
				obj.set_current_language(lang_code)
				name = obj.description
				if name:
					translations[lang_code] = name
			except:
				pass
		try:
			obj.set_current_language('ru')
		except:
			pass
		return translations

	def get_comment_count(self, obj):
		"""Get the count of comments and reviews for the product."""
		return obj.comments.count()

	def get_comment_and_review(self, obj):
		"""Get the comments and reviews for the product."""
		comments = obj.comments.all()
		return CommentAndReviewProductSerializer(comments, many=True, context=self.context).data

	def get_total_rating(self, obj):
		"""Calculate the total rating for the product."""
		if obj.comments.exists():
			total_rating = sum(comment.review_rating for comment in obj.comments.all())
			return total_rating / obj.comments.count()
		return 0.0


class CommentAndReviewProductCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = CommentAndReviewProduct
		fields = ['id', 'product', 'full_name', 'content', 'review_rating']
		read_only_fields = ['id', 'created_at']

	def validate_product(self, value):
		"""Validate that the product exists."""
		if not value:
			raise serializers.ValidationError("Product is required.")
		if not Product.objects.filter(id=value.id).exists():
			raise serializers.ValidationError("Product does not exist.")
		return value

	def validate_review_rating(self, value):
		"""Validate review rating is between 1 and 5."""
		if value < 1 or value > 5:
			raise serializers.ValidationError("Review rating must be between 1 and 5.")
		return value
