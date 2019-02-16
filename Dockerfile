FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
#RUN pip install django-sslserver
ADD . /code
EXPOSE 80 443
ENTRYPOINT ./django_instances.sh
