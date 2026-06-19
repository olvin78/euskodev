from modeltranslation.translator import translator, TranslationOptions
from .models import Blog

class BlogTranslationOptions(TranslationOptions):
    fields = ('titulo', 'resumen')

translator.register(Blog, BlogTranslationOptions)
