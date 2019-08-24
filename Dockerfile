FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends gettext && apt-get clean && \
    pip install uwsgi && pip install coverage

WORKDIR /app

USER $MOD_WSGI_USER:$MOD_WSGI_GROUP
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . .


RUN python manage.py collectstatic --no-input


EXPOSE 8000

