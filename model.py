"""Quiz builder api mongo db models."""

from mongoengine import (BooleanField, Document, EmailField, EmbeddedDocument,
                         EmbeddedDocumentField, FloatField, IntField,
                         ListField, ReferenceField, SequenceField, StringField)


class User(Document):
    """User model."""

    email = EmailField(primary_key=True)
    first_name = StringField(required=True, min_length=3, max_length=30)
    last_name = StringField(required=True, min_length=3, max_length=30)
    password_hash = StringField(required=True)
    active = BooleanField(default=False)


class Answer(EmbeddedDocument):
    """Answer model."""

    identifier = SequenceField(primary_key=True)
    answer_text = StringField(required=True, max_length=255)
    is_correct = BooleanField()


class Question(EmbeddedDocument):
    """Embedded Question model."""

    identifier = SequenceField(primary_key=True)
    title = StringField(required=True, min_length=3, max_length=500)

    answers = ListField(EmbeddedDocumentField(Answer))


class Quiz(Document):
    """Quiz model."""

    identifier = SequenceField(primary_key=True)
    title = StringField(required=True, min_length=3, max_length=75)
    description = StringField(required=False, max_length=255)
    questions = ListField(EmbeddedDocumentField(Question))
    is_published = BooleanField(default=False)
    owner = ReferenceField(User)


# Quiz solution
###############################################


# Submitted answer
class AnswerSubmit(EmbeddedDocument):
    """Model used to submit an answer."""

    identifier = IntField(required=True)
    is_correct = BooleanField(default=False)


# Submitted question
class QuestionSubmit(EmbeddedDocument):
    """Model used to submit a question."""

    identifier = IntField(required=True)
    title = StringField(required=False, min_length=3, max_length=500)
    answers = ListField(EmbeddedDocumentField(AnswerSubmit))


# Quiz solution
class QuizSolution(Document):
    """Quiz solution model representing a solution for a given quiz."""

    identifier = SequenceField(primary_key=True)
    title = StringField(required=False, min_length=3, max_length=500)
    description = StringField(required=False, max_length=255)
    quiz = ReferenceField(Quiz)
    questions = ListField(EmbeddedDocumentField(QuestionSubmit))

    owner = ReferenceField(User)
    total_points = IntField(default=0)
    scored_points = FloatField(default=0.0)
