"""Quiz module functionality providing all
needed methods and logic for quiz api handling."""

import logging
from typing import List

from fastapi import HTTPException

from api.quiz import model
from model import Quiz


def validate(
    quiz: Quiz, quiz_submit: model.QuizSubmit
) -> [model.QuizValidationResult, None]:
    """Validates/scores a quiz.
    :param quiz: The quiz data
    :param quiz_submit: The submitted quiz data
    :return: Validation result with total and the reached points"""

    qvr = model.QuizValidationResult
    try:
        points = 0.0
        for que, ques in zip(get_questions(quiz, quiz_submit)):
            points = score_question(points, que, ques)

        total_points = get_total(quiz.questions)
        return qvr(total_points=total_points, points=points)
    except Exception as exc:
        logging.exception(str(exc))
        return None


def score_question(points, qu, qu_submit):
    answers, answers_submit = get_answers(qu, qu_submit)
    if is_single(qu):
        points += score_single(answers, answers_submit)
    else:
        points += score_multi(answers, answers_submit)
    return points


def get_questions(quiz, quiz_submit):
    """Helper method to sort questions.
    :param quiz: quiz data
    :param quiz_submit: submitted quiz data
    :return: quiz and submitted quiz sorted questions"""

    questions = sorted(quiz.questions, key=lambda x: x.identifier)

    questions_submitted = sorted(quiz_submit.questions, key=lambda x: x.identifier)

    return questions, questions_submitted


def get_answers(question, question_submitted):
    """Helper method to get answers for quiz questions and
    submitted quiz questions.
    :param question: quiz questions
    :param question_submitted: submitted quiz questions
    :return: quiz answers and submitted quiz answers"""

    qu_ans = question.answers
    answers = [x.is_correct for x in sorted(qu_ans, key=lambda x: x.identifier)]

    qu_sans = question_submitted.answers
    answers_submitted = [
        x.is_correct for x in sorted(qu_sans, key=lambda x: x.identifier)
    ]

    return answers, answers_submitted


def get_total(questions):
    """Helper method to get total quiz points.
    :param questions: quiz questions
    :return: quiz total points"""

    return len(questions)


def is_single(question):
    """Helper method to check is a given question is a single
    answer question.
    :param question: quiz question
    :return: True single answer question and False otherwise"""

    return sum(question.answers) == 1


def score_single(quiz_answers: List[bool], submitted_answers: List[bool]):
    """Score single answer question.
    :param submitted_answers: quiz question submitted answers
    :param quiz_answers: quiz question actual answers
    :return: answer score"""

    sum_correct = sum(submitted_answers)
    if sum_correct == 0:
        return 0

    if sum_correct > 1:
        raise HTTPException(
            status_code=400,
            detail="Multiple answers not allowed for single answer question",
        )

    return 1 if submitted_answers[quiz_answers.index(True)] else -1


def score_multi(quiz_answers: List[bool], submitted_answers: List[bool]):
    """Score multi answer question
    :param submitted_answers: question submitted answers
    :param quiz_answers: given quiz question actual answers
    :return: question answers score"""

    sum_correct = sum(submitted_answers)
    if sum_correct == 0:
        return 0

    right = sum_correct
    wrong = len(submitted_answers) - right

    right, wrong = 1 / right, -1 / wrong
    total_score = sum(
        q and right or wrong for q, a in zip(submitted_answers, quiz_answers) if a
    )

    return total_score


def get_quiz_solution(quiz_solution_data):
    """Helper method to create quiz solution object."""

    quiz_solution = model.QuizSolution(**quiz_solution_data)
    quiz_solution.identifier = quiz_solution_data["_id"]
    return quiz_solution
