FROM python:3.6-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN apk add --no-cache bash


COPY ./amdtelecom /amdtelecom

WORKDIR /amdtelecom

RUN pip install -r requirements/prod.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# COPY ./docker/python/entrypoint.sh /entrypoint.sh

# RUN chmod +x /entrypoint.sh

# ENTRYPOINT ["sh", "/entrypoint.sh"]