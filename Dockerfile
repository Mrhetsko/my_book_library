#
FROM python:3.11-slim


WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY ./app /app/app
COPY alembic.ini /app/
COPY alembic /app/alembic


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]