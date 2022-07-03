FROM python:3.9

WORKDIR /code


# install requirements
# COPY ./requirements.txt /code
RUN pip install pip --upgrade
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install -r /code/requirements.txt

EXPOSE 5000/tcp
EXPOSE 5000/udp

# web server
# COPY ./master_router.py /code/
# COPY ./flask_server /code/flask_server
# telegram
# COPY ./tg_router.py /code
# COPY ./telegram_server /code/telegram_server

CMD ["python", "master_router.py"]

ENV PYTHONPATH=./
