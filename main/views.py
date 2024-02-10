from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils.http import urlencode
from django.views import View
from django.views.generic import ListView, TemplateView

from main.models import Survey, Answer, History, Question, Result
from main.services import get_question, get_statistics


class SurveyListView(ListView):
    model = Survey


class QuestionView(LoginRequiredMixin, View):

    def get(self, request, pk, *args, **kwargs):
        questions = Question.objects.filter(survey=pk)
        answer = request.GET.get('answer')
        question = request.GET.get('question')

        current_question = get_question(questions, answer, question)

        if current_question is None:
            params = {
                'survey': pk
            }

            return redirect(
                f"{reverse('main:get_statistics')}?{urlencode(params)}"
            )

        else:
            return render(request, 'main/question.html',
                          context={'current_question': current_question})


class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = 'main/statistics.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        survey_pk = request.GET.get('survey')
        statistics = get_statistics(survey_pk)
        context['statistics'] = statistics

        return self.render_to_response(context)


@login_required
def answer_question(request, pk):
    answer = get_object_or_404(Answer, pk=pk)

    try:
        history = History.objects.get(survey=answer.question.survey, user=request.user)
    except History.DoesNotExist:
        history = History.objects.create(survey=answer.question.survey, user=request.user)

    Result.objects.create(history=history, answer=answer)

    params = {
        'answer': answer.pk, 'question': answer.question.pk
    }

    return redirect(
        f"{reverse('main:survey_detail', kwargs={'pk': answer.question.survey.pk})}?{urlencode(params)}"
    )
