from django.shortcuts import get_object_or_404

from main.models import Question, Answer


def get_question(questions, answer, question):
    """
    Возвращает вопрос, который нужно задать
    :param questions: вопросы данного опросника
    :param answer: ответ, на предыдущий вопрос
    :param question: предыдущий вопрос
    :return: объект Question или None
    """
    # Проверяем задавались ли уже вопросы
    if answer is None and question is None:
        current_question = questions.filter(answer=None).filter(question=None).first()
        return current_question

    # Проверяем есть ли у вопроса зависимый вопрос
    if question:
        question = get_object_or_404(Question, pk=question)

        try:
            current_question = questions.get(id=question.question_dependent_question.id)
            return current_question
        except Question.question_dependent_question.RelatedObjectDoesNotExist:
            pass

    # Проверяем есть ли у ответа зависимый вопрос
    if answer:
        answer = get_object_or_404(Answer, pk=answer)

        try:
            current_question = questions.get(answer=answer)
            return current_question
        except Question.DoesNotExist:
            return
