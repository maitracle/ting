from django.contrib import admin
from django.contrib.admin import register

from profiles.models import QuestionList, QuestionItem


@register(QuestionList)
class QuestionListAdmin(admin.ModelAdmin):
    list_display = ('name', 'university', 'season', 'version')
    list_filter = ('university',)


@register(QuestionItem)
class QuestionItem(admin.ModelAdmin):
    list_display = ('name', )
