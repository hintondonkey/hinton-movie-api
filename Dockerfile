FROM python:3.10.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /code
WORKDIR /code
RUN python3.10 -m pip install --no-cache-dir --upgrade \
    pip \
    setuptools \
    wheel

RUN addgroup --system dokku \
    && adduser --system --ingroup dokku dokku

COPY requirements.txt /code/

RUN pip install --no-cache-dir  -r requirements.txt && rm -rf /var/lib/apt/lists/*
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput --clear
RUN chmod -R 777 /code/static/
# RUN chmod -R 777 /code/staticfiles/
RUN chown -R dokku:dokku /code/
# RUN chown -R dokku:dokku /code/media/
USER dokku

# COPY ./entrypoint.sh /
# ENTRYPOINT ["sh", "/entrypoint.sh"]

EXPOSE 8000
# Run application
# CMD gunicorn phongthuy_thanhnhan.wsgi:application --bind 0.0.0.0:8000
CMD [ "gunicorn", "code:code" ]