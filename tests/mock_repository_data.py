# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=E501

"""Mock repository data for user, quiz."""

from model import Answer, Question, Quiz, User

# password_hash is a hash of: _Hard_pass1

mock_user_data = {
    "john@wick.com": User(
        email="john@wick.com",
        first_name="John",
        last_name="Wick",
        active=True,
        password_hash="$5$rounds=535000$6QxS6Vxn3C5uufw2$pMApAxokjLzhEDwaqY..eD/CF2PnYDXBomX5b35XmzD",
    ),
    "al.pacino@gmail.com": User(
        email="al.pacino@gmail.com",
        first_name="Al",
        last_name="Pacino",
        active=True,
        password_hash="$5$rounds=535000$6QxS6Vxn3C5uufw2$pMApAxokjLzhEDwaqY..eD/CF2PnYDXBomX5b35XmzD",
    ),
}

mock_quiz_data = {
    1: Quiz(
        identifier=1,
        title="Sample Quiz Capital of USA.",
        description="Some quiz.",
        owner=mock_user_data["john@wick.com"],
        questions=[
            Question(
                identifier=1,
                title="What is the Capital of the United States.",
                answers=[
                    Answer(identifier=111, answer_text="Paris", is_correct=False),
                    Answer(identifier=112, answer_text="Egypt", is_correct=False),
                    Answer(
                        identifier=113, answer_text="Washington DC", is_correct=True
                    ),
                    Answer(identifier=114, answer_text="Austin", is_correct=False),
                ],
            )
        ],
    ),
    2: Quiz(
        identifier=2,
        title="Sample Quiz Two Capital of Poland.",
        description="Some quiz.",
        owner=mock_user_data["john@wick.com"],
        questions=[
            Question(
                identifier=2,
                title="What is the Capital of Poland.",
                answers=[
                    Answer(identifier=221, answer_text="Berlin", is_correct=False),
                    Answer(identifier=222, answer_text="Moscow", is_correct=False),
                    Answer(identifier=223, answer_text="Poznan", is_correct=False),
                    Answer(identifier=4224, answer_text="Warsaw", is_correct=True),
                ],
            )
        ],
    ),
    3: Quiz(
        identifier=3,
        title="Sample Quiz Three.",
        description="Some quiz.",
        owner=mock_user_data["al.pacino@gmail.com"],
        questions=[
            Question(
                identifier=1,
                title="What countries use English as native language.",
                answers=[
                    Answer(
                        identifier=331, answer_text="United States", is_correct=True
                    ),
                    Answer(identifier=332, answer_text="Germany", is_correct=False),
                    Answer(identifier=333, answer_text="Canada", is_correct=True),
                    Answer(identifier=334, answer_text="England", is_correct=True),
                ],
            )
        ],
    ),
    4: Quiz(
        identifier=4,
        title="Sample Quiz Four.",
        description="Some quiz.",
        owner=mock_user_data["al.pacino@gmail.com"],
        is_published=True,
        questions=[
            Question(
                identifier=1,
                title="What car models does BMW produce.",
                answers=[
                    Answer(identifier=331, answer_text="330I", is_correct=True),
                    Answer(identifier=332, answer_text="875I", is_correct=False),
                    Answer(identifier=333, answer_text="X9", is_correct=False),
                    Answer(identifier=334, answer_text="M3", is_correct=True),
                    Answer(identifier=334, answer_text="M5", is_correct=True),
                ],
            )
        ],
    ),
    5: Quiz(
        identifier=4,
        title="Sample Quiz Five.",
        description="Some quiz.",
        owner=mock_user_data["al.pacino@gmail.com"],
        questions=[
            Question(
                identifier=1,
                title="What is the currency in Poland.",
                answers=[
                    Answer(identifier=331, answer_text="Rubel", is_correct=False),
                    Answer(identifier=332, answer_text="Yen", is_correct=False),
                    Answer(identifier=333, answer_text="Zloty", is_correct=True),
                    Answer(identifier=334, answer_text="Dollar", is_correct=False),
                    Answer(identifier=334, answer_text="Frank", is_correct=True),
                ],
            )
        ],
    ),
}
