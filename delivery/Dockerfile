FROM python:3.11

WORKDIR /app

ADD . /app
ADD uszips.csv /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENV NAME World

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
