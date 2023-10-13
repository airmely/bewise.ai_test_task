from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, index=True)
    id_question = Column(Integer)
    text = Column(String, index=True)
    answer = Column(String)
    created_at = Column(String)
