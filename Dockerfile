FROM python:3.9-slim

WORKDIR /code/src

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./src /code/src

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
