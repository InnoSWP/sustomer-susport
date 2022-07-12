FROM python:3.9-slim

WORKDIR /code

# install requirements
COPY ./requirements.txt /code
RUN pip install pip --upgrade --no-cache-dir && pip install --no-cache-dir  -r /code/requirements.txt

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
