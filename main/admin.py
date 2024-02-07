from django.contrib import admin

from main.models import Question, Survey, Answer


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionInline(admin.TabularInline):
    model = Question
    inlines = [AnswerInline]


@admin.register(Question)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['id', 'survey', 'text', 'question', 'answer']
    search_fields = ['id', 'name', 'survey', 'text']
    list_filter = ['survey']
    inlines = [AnswerInline]


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['id', 'name']
    inlines = [QuestionInline]
