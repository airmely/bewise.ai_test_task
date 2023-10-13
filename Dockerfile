FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY ./app/ /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
