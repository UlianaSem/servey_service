from django.db.models import (Model, CharField, TextField, ForeignKey, CASCADE,
                              UniqueConstraint, SET_NULL, OneToOneField)


class Survey(Model):
    name = CharField(max_length=255, verbose_name='название опроса')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'опрос'
        verbose_name_plural = 'опросы'


class Question(Model):
    survey = ForeignKey(Survey, on_delete=CASCADE, related_name='questions', verbose_name='опрос')
    text = TextField(verbose_name='текст вопроса')

    question = OneToOneField('Question', on_delete=SET_NULL, related_name='question_dependent_question',
                             verbose_name='вопрос, от которого зависит данный вопрос', null=True, blank=True)
    answer = OneToOneField('Answer', on_delete=SET_NULL, related_name='answer_dependent_question',
                           verbose_name='ответ, от которого зависит данный вопрос', null=True, blank=True)

    def __str__(self):
        return f'{self.survey.name}: {self.text[:100]}'

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'
        constraints = [
            UniqueConstraint(
                fields=('survey', 'text',),
                name='Unique survey and text', ),
        ]


class Answer(Model):
    question = ForeignKey(Question, on_delete=CASCADE, related_name='answers', verbose_name='вопрос')
    text = CharField(max_length=300, verbose_name='текст ответа')

    def __str__(self):
        return f'{self.question.text[:100]}: {self.text[:100]}'

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'
        constraints = [
            UniqueConstraint(
                fields=('question', 'text',),
                name='Unique question and text', ),
        ]
