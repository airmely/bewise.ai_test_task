from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """
    Класс, представляющий запрос на получение вопросов.
    Атр.:
        questions_num (int): Кол-ство вопросов, которые
                             требуется получить.
    """
    questions_num: int
