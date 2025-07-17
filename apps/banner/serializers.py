from rest_framework import serializers

from apps.banner.models import Banner, Partner, Advertisement, Blog


class BannerSerializer(serializers.ModelSerializer):
	translated_title = serializers.SerializerMethodField()
	translated_description = serializers.SerializerMethodField()

	class Meta:
		model = Banner
		fields = ['id', 'translated_title', 'translated_description', 'image', 'link', 'created_at']
		read_only_fields = ['created_at']

	def get_translated_title(self, obj):
		"""Get all translations for all languages"""
		translations = {}
		for lang_code, lang_name in [('ru', 'russian'), ('en', 'english'), ('uz', 'uzbek'), ('kk', 'kazakh'), ('ko', 'korean')]:
			try:
				obj.set_current_language(lang_code)
				title = obj.title
				if title:
					translations[lang_code] = title
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
				description = obj.description
				if description:
					translations[lang_code] = description
			except:
				pass
		try:
			obj.set_current_language('ru')
		except:
			pass
		return translations


class PartnerSerializer(serializers.ModelSerializer):
	translated_title = serializers.SerializerMethodField()
	translated_description = serializers.SerializerMethodField()

	class Meta:
		model = Partner
		fields = ['id', 'translated_title', 'translated_description', 'image', 'link', 'created_at']
		read_only_fields = ['created_at']

	def get_translated_title(self, obj):
		"""Get all translations for all languages"""
		translations = {}
		for lang_code, lang_name in [('ru', 'russian'), ('en', 'english'), ('uz', 'uzbek'), ('kk', 'kazakh'), ('ko', 'korean')]:
			try:
				obj.set_current_language(lang_code)
				title = obj.title
				if title:
					translations[lang_code] = title
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
				description = obj.description
				if description:
					translations[lang_code] = description
			except:
				pass
		try:
			obj.set_current_language('ru')
		except:
			pass
		return translations


class AdvertisementSerializer(serializers.ModelSerializer):
	translated_title = serializers.SerializerMethodField()
	translated_description = serializers.SerializerMethodField()

	class Meta:
		model = Advertisement
		fields = ['id', 'translated_title', 'translated_description', 'image', 'link', 'created_at']
		read_only_fields = ['created_at']

	def get_translated_title(self, obj):
		"""Get all translations for all languages"""
		translations = {}
		for lang_code, lang_name in [('ru', 'russian'), ('en', 'english'), ('uz', 'uzbek'), ('kk', 'kazakh'), ('ko', 'korean')]:
			try:
				obj.set_current_language(lang_code)
				title = obj.title
				if title:
					translations[lang_code] = title
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
				description = obj.description
				if description:
					translations[lang_code] = description
			except:
				pass
		try:
			obj.set_current_language('ru')
		except:
			pass
		return translations


class BlogSerializer(serializers.ModelSerializer):
	translated_title = serializers.SerializerMethodField()
	translated_content = serializers.SerializerMethodField()

	class Meta:
		model = Blog
		fields = ['id', 'translated_title', 'translated_content', 'image', 'link', 'created_at']
		read_only_fields = ['created_at']

	def get_translated_title(self, obj):
		"""Get all translations for all languages"""
		translations = {}
		for lang_code, lang_name in [('ru', 'russian'), ('en', 'english'), ('uz', 'uzbek'), ('kk', 'kazakh'), ('ko', 'korean')]:
			try:
				obj.set_current_language(lang_code)
				title = obj.title
				if title:
					translations[lang_code] = title
			except:
				pass
		try:
			obj.set_current_language('ru')
		except:
			pass
		return translations

	def get_translated_content(self, obj):
		"""Get all translations for all languages"""
		translations = {}
		for lang_code, lang_name in [('ru', 'russian'), ('en', 'english'), ('uz', 'uzbek'), ('kk', 'kazakh'), ('ko', 'korean')]:
			try:
				obj.set_current_language(lang_code)
				content = obj.content
				if content:
					translations[lang_code] = content
			except:
				pass
		try:
			obj.set_current_language('ru')
		except:
			pass
		return translations
