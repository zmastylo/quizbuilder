# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=R0903
# pylint: disable=N805

"""Quiz module models."""

from typing import List, Optional

from pydantic import ValidationError, validator
from pydantic.main import BaseModel

from core.config import get_config


class BaseAnswer(BaseModel):
    """Base class for answer model."""

    answer_text: str
    is_correct: bool


class NewAnswer(BaseAnswer):
    """New answer model: used to submit new quiz."""


class Answer(BaseAnswer):
    """Answer model."""

    identifier: Optional[int]


class BaseQuestion(BaseModel):
    """Base question model."""

    title: str


class NewQuestion(BaseQuestion):
    """New question model: used with submission of
    new quiz."""

    answers: List[NewAnswer] = []

    @validator("answers", each_item=False)
    def answer_validation(cls, answers: List[NewAnswer]):
        """Pydantic Validation -> checks if at least one
        correct answer is provided and there is at most five answers.
        :param answers: List of answers
        :return: Returns the validated answers"""

        max_answers = get_config().MAX_ANSWERS_PER_QUESTION
        if len(answers) > max_answers:
            raise ValidationError(
                f"Number of answers must be less then:{max_answers}", NewQuestion
            )

        correct_answer_ct = sum(1 for a in answers if a.is_correct)
        if correct_answer_ct == 0:
            raise ValidationError(
                "At least one correct answer is required", NewQuestion
            )
        return answers


class Question(BaseQuestion):
    """Question model: used as a response model for
    quiz question."""

    identifier: Optional[int]
    answers: List[Answer]


class BaseQuiz(BaseModel):
    """Base class for quiz model."""

    title: str
    description: str


class NewQuiz(BaseQuiz):
    """New quiz model: used as model for quiz creation."""

    is_published: bool = False
    questions: List[NewQuestion] = []

    @validator("questions", each_item=False)
    def questions_validator(cls, questions: List[NewQuestion]):
        """Pydantic Validation checks if at least one question is
        provided, and numbers of questions less than MAX_QUESTIONS.
        :param questions: List of questions
        :return: Returns the validated questions"""

        max_questions = get_config().MAX_QUESTIONS
        if len(questions) > max_questions:
            raise ValidationError(
                f"Number of questions must be less then:{max_questions}", NewQuiz
            )
        if len(questions) == 0:
            raise ValidationError("Please specify at least one question", NewQuiz)
        return questions


class Quiz(BaseQuiz):
    """Quiz model used a response object for create and update quiz
    endpoints."""

    identifier: Optional[int]
    questions: List[Question] = []
    owner: str


class QuizPublish(BaseModel):
    """Quiz publish model: used to publish a given quiz."""

    identifier: Optional[int]
    is_published: bool


class AnswerSubmit(BaseModel):
    """Answer submit model."""

    identifier: Optional[int]
    is_correct: bool


class QuestionSubmit(BaseModel):
    """Question submit model."""

    identifier: Optional[int]
    title: Optional[str]
    answers: List[AnswerSubmit] = []


class QuizSubmit(BaseModel):
    """Quiz submit model used for quiz submission."""

    identifier: Optional[int]
    questions: List[QuestionSubmit] = []


class QuizSolution(QuizSubmit):
    """Quiz solution model used as response model for
    quiz submission."""

    total_points: int
    scored_points: float


class QuizValidationResult(BaseModel):
    """Quiz validation/score model."""

    total_points: int
    points: float
