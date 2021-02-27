# deployment
# bunlar Dockerfile daydi

# FROM python:alpine

FROM python:3.6-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
# pip install psycopg2

ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers
RUN pip install -r /requirements.txt
RUN apk del .tmp

RUN mkdir /app
COPY ./amdtelecom /app

WORKDIR /app
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]

asagidakilar docker folderindeki
python folderini icindeki entrypoint.sh -dakilardi

#!/bin/bash

exec python manage.py runserver 0.0.0.0:8000

# check who owns the working directory
# USER_ID=$(stat -c "%u" $PWD)

# # set the python run uid to the user id we just retrieved
# PYTHON_RUN_UID=${PYTHON_RUN_UID:=${USER_ID}}
# PYTHON_RUN_USER=${PYTHON_RUN_USER:=fuad}
# PYTHON_RUN_GROUP=${PYTHON_RUN_GROUP:=fuad}

# # test to see if the user already exists
# PYTHON_RUN_USER_TEST=$(grep "[a-zA-Z0-9\-\_]*:[a-zA-Z]:${PYTHON_RUN_UID}:" /etc/passwd)


# # Update the user to the configured UID and group
# if [ -n "${PYTHON_RUN_USER_TEST}" ]; then
#     echo "Update user '$PYTHON_RUN_USER'"

#     usermod -l ${PYTHON_RUN_USER} $(id -un ${PYTHON_RUN_UID})
#     usermod -u $PYTHON_RUN_UID -g $PYTHON_RUN_GROUP $PYTHON_RUN_USER

# # Else create the user with the configured UID and group
# else
#     echo "Create user '$PYTHON_RUN_USER'"

#     # Create the user with the corresponding group
#     mkdir -p /home/$PYTHON_RUN_USER
#     groupadd $PYTHON_RUN_GROUP
#     useradd -u $PYTHON_RUN_UID -g $PYTHON_RUN_GROUP -d /home/$PYTHON_RUN_USER $PYTHON_RUN_USER
#     chown $PYTHON_RUN_USER:$PYTHON_RUN_GROUP /home/$PYTHON_RUN_USER
# fi

# export HOME=/home/$PYTHON_RUN_USER



# echo "Running command '$*'"
# exec su -p - ${PYTHON_RUN_USER} -s /bin/bash -c "$*"