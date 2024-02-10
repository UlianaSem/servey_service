from django.urls import path

from main.apps import MainConfig
from main.views import SurveyListView, QuestionView, answer_question, StatisticsView

app_name = MainConfig.name

urlpatterns = [
    path('', SurveyListView.as_view(), name='survey_list'),
    path('survey/<int:pk>/', QuestionView.as_view(), name='survey_detail'),
    path('answer_question/<int:pk>/', answer_question, name='answer_question'),
    path('statistics/', StatisticsView.as_view(), name='get_statistics'),
]
