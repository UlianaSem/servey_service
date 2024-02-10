from django.db import connection
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


def get_statistics(survey_pk):
    """
    Возвращает статистику по опросу, а именно:
    1. Общее кол-во участников опроса (например, 100)
    2. Для каждого вопроса:
    2.1. Кол-во ответивших и их доля от общего кол-ва участников опроса
    2.2. Порядковый номер вопроса по кол-ву ответивших
    2.3. Кол-во ответивших на каждый из вариантов ответа и их доля от общего кол-ва ответивших на этот вопрос после
    завершения опроса
    :param survey_pk: id опроса
    :return: словарь со статистикой
    """
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT COUNT(DISTINCT(main_history.user_id)) from main_history WHERE main_history.survey_id = %s",
            [survey_pk])
        total_number = cursor.fetchone()[0]

        cursor.execute(
            """SELECT main_question.text, COUNT(DISTINCT(main_history.user_id)) AS user_count,
            ROUND(COUNT(DISTINCT(main_history.user_id))/%s::NUMERIC, 2) AS proportion,
            DENSE_RANK() OVER(ORDER BY COUNT(DISTINCT(main_history.user_id)) DESC) as rank
            FROM main_history
            INNER JOIN main_result ON main_history.id = main_result.history_id
            INNER JOIN main_answer ON main_result.answer_id = main_answer.id
            LEFT JOIN main_question ON main_answer.question_id = main_question.id
            WHERE main_history.survey_id = %s
            GROUP BY main_question.text""", [total_number, survey_pk]
        )

        data = cursor.fetchall()
        questions = [
            {'question_text': line[0], 'user_count': line[1], 'proportion': line[2], 'rank': line[3]} for line in data
        ]

        cursor.execute(
            """
            WITH question_user AS (SELECT main_question.id, COUNT(DISTINCT(main_history.user_id)) AS user_count
            FROM main_history
            INNER JOIN main_result ON main_history.id = main_result.history_id
            INNER JOIN main_answer ON main_result.answer_id = main_answer.id
            LEFT JOIN main_question ON main_answer.question_id = main_question.id
            WHERE main_history.survey_id = %s
            GROUP BY main_question.id)
            SELECT main_answer.text, 
            main_question.text,
            COUNT(DISTINCT(main_history.user_id)), 
            ROUND(COUNT(DISTINCT(main_history.user_id))/question_user.user_count::NUMERIC, 2) AS proportion
            FROM main_history
            INNER JOIN main_result ON main_history.id = main_result.history_id
            LEFT JOIN main_answer ON main_result.answer_id = main_answer.id
            LEFT JOIN main_question ON main_answer.question_id = main_question.id
            INNER JOIN question_user ON main_question.id = question_user.id
            WHERE main_history.survey_id = %s
            GROUP BY main_answer.text, main_question.text, question_user.user_count""", [survey_pk, survey_pk]
        )

        data = cursor.fetchall()
        answers = [
            {'answer_text': line[0], 'question_text': line[1], 'user_count': line[2], 'proportion': line[3]} for line in
            data
        ]

    statistics = {
        'total_number': total_number,
        'questions': questions,
        'answers': answers
    }

    return statistics
