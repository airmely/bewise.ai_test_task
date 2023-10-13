import httpx
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
import schemas
from db import SessionLocal, engine
from models import Question


class LazyDbInit:
    """
    Класс для инициализации базы данных.
        Этот класс предназначен для инициализации базы данных в ленивом режиме,
        то есть только при первом вызове метода `initialize()`.
        Он использует SQLAlchemy для создания таблиц в базе данных, определенных в моделях данных.

    Атр.:
        is_initizalized (bool): Флаг, который указывает, была ли база данных инициализирована.
    """
    is_initizalized = False

    @classmethod
    def initialize(cls):
        """
        Инициализирует базу данных.
        """
        if not cls.is_initizalized:
            models.Base.metadata.create_all(bind=engine)
            cls.is_initizalized = True


app = FastAPI()  # экземпляр класса FastAPI


def get_db():
    """
    Функция для получения экземпляра базы данных.
    """
    LazyDbInit.initialize()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_question(
        db: Session,
        question: Question
) -> Question | None:
    """
    Функция, которая сохраняет вопрос в базе данных,
    если вопрос с таким text не существует.
    Пар.:
        db (Session): Экземпляр базы данных SQLAchemy.
        question (Question): Вопрос для сохранения.
    Возвращает:
        Question: Сохраненный вопрос, который успешно сохранен, иначе None.
    """
    existing_question = db.query(Question).filter(Question.text == question.text).first()
    if existing_question:
        return None
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


async def choice_of_question(
        db: Session,
        question_num: int
) -> list[Question]:
    """
    Выбирает случайные вопросы из внешнего источника и сохраняет их в базе данных.
    Пар.:
        db (Session): Экземпляр базы данных SQLAlchemy.
        question_num (int): Количество случайных вопросов для выбора.
    Возвращает:
    list[Question]: Список сохраненных вопросов, если успешно сохранены.
    """
    questions = []
    while len(questions) < question_num:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'https://jservice.io/api/random?count={question_num}')
            data = response.json()
            questions_data = data[0]
            question = Question(
                id_question=questions_data['id'],
                text=questions_data['question'],
                answer=questions_data['answer'],
                created_at=questions_data['created_at'],
            )
            saved_question = save_question(db, question)
            if saved_question:
                questions.append(saved_question)

    return questions


@app.post('/get_questions/')
async def get_questions(
        request: schemas.QuestionRequest,
        db: Session = Depends(get_db)
) -> dict:
    """
    Обработчик POST-запроса для получения случайных вопросов.

    Пар.:
        request (QuestionRequest): Модель запроса, содержащая количество вопросов для получения.
        db (Session): Экземпляр базы данных SQLAlchemy.

    Возвращает:
        dict: Словарь с вопросами, если запрос успешно обработан, или сообщением об ошибке.
    """
    questions_num = request.questions_num
    if questions_num < 1:
        return {'error': 'Количество вопросов должно быть не менее 1'}

    questions = await choice_of_question(db, questions_num)
    return {'questions': [question.text for question in questions]}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
