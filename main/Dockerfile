FROM tiangolo/uvicorn-gunicorn:python3.10-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /code

COPY poetry.lock pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./app /code/app
COPY ./alembic /code/alembic
COPY alembic.ini /code/alembic.ini
COPY resetdb.sh /resetdb.sh
COPY start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]