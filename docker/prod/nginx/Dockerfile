FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf

COPY ./docker/prod/nginx/django_amdtelecom.conf /etc/nginx/conf.d/default.conf
