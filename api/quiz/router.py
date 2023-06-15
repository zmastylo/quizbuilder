"""Quiz module routing and handling logic."""

import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from api.auth.main import get_current_active_user
from api.quiz import model
from api.quiz.main import get_quiz_solution, validate
from core.exception import NotFoundError, UnauthorizedError
from database.repository import RepositoryFactory, get_repository
from model import Quiz, QuizSolution, User
from util import first_item, get_query_params

quiz_router = APIRouter(prefix="/quiz", tags=["Quiz"])


@quiz_router.get("/", response_model=List[model.Quiz])
def read_quizzes(
    title: str = None,
    description: str = None,
    owner_email: str = None,
    repo: RepositoryFactory = Depends(get_repository),
):
    """Quiz query endpoint. For each parameter the query returns
    all quizzes that contain a given search value in that parameter i.e.
    description = 'Capital of' --> the query would return all quizzes that
    contain 'Capital of' if their description.

    :param title: quiz title
    :param description: quiz description
    :param owner_email: quiz owner email
    :param repo: repository factory
    :return: List of quizzes"""

    query_params = get_query_params(title, description, owner_email)
    result = repo.quiz.filter(**query_params)
    result = json.loads(result.to_json())
    return result


@quiz_router.get("/solutions", response_model=List[model.QuizSolution])
def read_solutions(
    title: str = None,
    description: str = None,
    owner_email: str = None,
    repo: RepositoryFactory = Depends(get_repository),
):
    """Quiz solutions endpoint. For each parameter the query returns
    all quizzes that contain a given search value in that parameter i.e.
    description = 'Capital of' --> the query would return all solutions that
    contain 'Capital of' if their description.

    :param title: quiz title
    :param description: quiz description
    :param owner_email: quiz owner email
    :param repo: repository factory
    :return: List of quiz solution"""

    query_params = get_query_params(title, description, owner_email)
    query_result = repo.quiz_solution.filter(**query_params)
    quiz_solution_list = json.loads(query_result.to_json())
    response = [get_quiz_solution(item) for item in quiz_solution_list]
    return response


@quiz_router.get("/{quiz_id}", response_model=model.Quiz)
async def get_quiz(quiz_id: int, repo: RepositoryFactory = Depends(get_repository)):
    """Read/get quiz endpoint.
    :param quiz_id: Quiz ID
    :param repo: repository factory
    :return: Quiz object"""

    quiz = repo.quiz.get(quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz does not exist")

    kwargs = {"use_db_field": False}
    json_quiz = json.loads(quiz.to_json(**kwargs))
    return model.Quiz(**json_quiz)


@quiz_router.post("/", response_model=model.Quiz)
async def create_quiz(
    new_quiz: model.NewQuiz,
    current_user: User = Depends(get_current_active_user),
    repo: RepositoryFactory = Depends(get_repository),
):
    """Quiz creation endpoint
    :param new_quiz: Quiz data
    :param current_user: Current user
    :param repo: repository factory
    :return: Returns the created quiz"""

    quiz_to_create = Quiz(
        **new_quiz.dict(),
        owner=current_user.email,
    )

    quiz_created = repo.quiz.persist(quiz_to_create)
    kwargs = {"use_db_field": False}
    json_quiz = json.loads(quiz_created.to_json(**kwargs))
    return model.Quiz(**json_quiz)


@quiz_router.put("/publish/{quiz_id}", response_model=model.QuizPublish)
async def publish_quiz(
    quiz_id: int,
    current_user: User = Depends(get_current_active_user),
    repo: RepositoryFactory = Depends(get_repository),
):
    """Quiz publishing endpoint. After quiz is created, a quiz may
    not be published in which case it isONLY visible to the owner
    of a quiz. Quiz publishing is a simple operation that sets
    is_published to True for a created quiz.
    :param quiz_id: Quiz id to publish
    :param current_user: current authenticated user
    :param repo: repository factory
    :return: Returns the published quiz id and status of publishing"""

    quiz_to_publish = repo.quiz.get(quiz_id)
    if quiz_to_publish is None:
        raise HTTPException(status_code=404, detail="Quiz does not exist!")

    if quiz_to_publish.owner.email != current_user.email:
        raise HTTPException(status_code=401)

    quiz_to_publish.is_published = True
    return model.QuizPublish(**{"identifier": quiz_id, "is_published": True})


@quiz_router.put("/{quiz_id}", response_model=model.Quiz)
async def update_quiz(
    quiz_id: int,
    quiz_update_data: model.NewQuiz,
    current_user: User = Depends(get_current_active_user),
    repo: RepositoryFactory = Depends(get_repository),
):
    """Quiz update endpoint.
    :param quiz_id: Quiz ID
    :param quiz_update_data: Quiz update data
    :param current_user: Current user
    :param repo: repository factory
    :return: Returns the updated quiz"""

    quiz_to_update: Quiz = repo.quiz.get(quiz_id)
    if quiz_to_update is None:
        raise HTTPException(status_code=404, detail="Quiz does not exist!")
    if quiz_to_update.owner.email != current_user.email:
        raise HTTPException(status_code=401)

    if quiz_to_update.is_published:
        raise HTTPException(status_code=400, detail="Cannot update published quiz")

    updated_quiz = Quiz(
        **quiz_update_data.dict(exclude={"identifier"}),
        identifier=quiz_id,
        owner=current_user.email,
    )

    repo.quiz.persist(updated_quiz)
    kwargs = {"use_db_field": False}
    json_quiz = json.loads(updated_quiz.to_json(**kwargs))
    return model.Quiz(**json_quiz)


@quiz_router.post("/validate", response_model=model.QuizValidationResult)
async def validate_quiz(
    quiz_submit: model.QuizSubmit,
    current_user: User = Depends(get_current_active_user),
    repo: RepositoryFactory = Depends(get_repository),
):
    """Quiz validation endpoint.
    :param quiz_submit: Quiz submit data
    :param current_user: current authorized user
    :param repo: repository factory
    :return: Quiz validation result"""

    quiz_to_take: Quiz = repo.quiz.get(quiz_submit.identifier)
    if quiz_to_take is None:
        raise HTTPException(status_code=404, detail="Quiz does not exist")

    if quiz_to_take.owner.email == current_user.email:
        raise HTTPException(status_code=403, detail="Not allowed to take his own quiz")

    if not quiz_to_take.is_published:
        raise HTTPException(
            status_code=401, detail="Not allowed to take unpublished quiz"
        )

    query_params = {"owner": current_user.email, "quiz": quiz_submit.identifier}

    quiz_already_taken = repo.quiz_solution.filter(**query_params)
    if first_item(quiz_already_taken) is not None:
        raise HTTPException(
            status_code=401, detail="Not allowed to take same quiz more then once"
        )

    validation_result = validate(quiz_to_take, quiz_submit)
    if validation_result is None:
        raise HTTPException(status_code=400)

    quiz_solution: QuizSolution = QuizSolution(
        **quiz_submit.dict(exclude={"identifier"}),
        quiz=quiz_to_take.identifier,
        owner=current_user.email,
        title=quiz_to_take.title,
        description=quiz_to_take.description,
        total_points=validation_result.total_points,
        scored_points=validation_result.points,
    )

    result = repo.quiz_solution.persist(quiz_solution)
    if result is None:
        raise HTTPException(status_code=500, detail="Unable to persist quiz solution")

    return validation_result


@quiz_router.delete("/{quiz_id}", responses={401: {"model": dict}})
async def delete_quiz(
    quiz_id: int,
    current_user: User = Depends(get_current_active_user),
    repo: RepositoryFactory = Depends(get_repository),
):
    """Quiz delete endpoint.
    :param quiz_id: Quiz ID
    :param current_user: Current User
    :param repo: repository factory
    :return: 200 if OK"""

    quiz_to_delete = repo.quiz.get(quiz_id)
    if quiz_to_delete is None:
        raise NotFoundError("Quiz does not exist")
    if quiz_to_delete.owner.email != current_user.email:
        raise UnauthorizedError()

    repo.quiz.delete(quiz_to_delete)
    return {"quiz_id": quiz_id, "is_deleted": True}
