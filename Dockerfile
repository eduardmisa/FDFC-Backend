FROM python:3.7
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ADD . /code
COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 9999
RUN python manage.py migrate
