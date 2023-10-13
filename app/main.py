import httpx
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
import schemas
from db import SessionLocal, engine
from models import Question


class LazyDbInit:
    is_initizalized = False

    @classmethod
    def initialize(cls):
        if not cls.is_initizalized:
            models.Base.metadata.create_all(bind=engine)
            cls.is_initizalized = True


app = FastAPI()


def get_db():
    LazyDbInit.initialize()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_question(db: Session, question: Question):
    existing_question = db.query(Question).filter(Question.text == question.text).first()
    if existing_question:
        return None
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


async def choice_of_question(db: Session, question_num: int):
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
async def get_questions(request: schemas.QuestionRequest, db: Session = Depends(get_db)):
    questions_num = request.questions_num
    if questions_num < 1:
        return {'error': 'Количество вопросов должно быть не менее 1'}

    questions = await choice_of_question(db, questions_num)
    return {'questions': [question.text for question in questions]}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
