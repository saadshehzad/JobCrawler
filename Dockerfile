FROM python:3.9-slim

WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY .env /code/
COPY ./src /code/src

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
