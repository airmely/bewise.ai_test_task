from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()  # экземпляр базового класса


class Question(Base):
    """
    Класс, представляющий собой модели данных для запроса
    """
    __tablename__ = 'questions'
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    id_question: Column[int] = Column(Integer)
    text: Column[str] = Column(String, index=True)
    answer: Column[str] = Column(String)
    created_at: Column[str] = Column(String)
