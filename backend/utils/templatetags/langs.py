# coding:utf-8
from django.utils.translation import get_language_info
from django.conf import settings

from django import template
register = template.Library()

LANGUAGES = []
for lang_code in settings.LANGUAGES_SUPPORTED:
    LANGUAGES.append(get_language_info(lang_code))


@register.inclusion_tag('parts/languages_select_part.html')
def language_select(default):
    return {'languages': LANGUAGES, 'default': default}


# 在模板中调用 setting 中的值，用法如：{% settings_value "LANGUAGE_CODE" %}
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")