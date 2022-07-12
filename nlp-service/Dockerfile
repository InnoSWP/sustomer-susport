FROM python:3.9-slim

WORKDIR /code


# install requirements
COPY ./requirements.txt /code
COPY ./nlp/similarity_providers.py /code/nlp/similarity_providers.py

RUN pip install pip --upgrade --no-cache-dir &&\
			pip --no-cache-dir install -r /code/requirements.txt &&\
			python ./nlp/similarity_providers.py

EXPOSE 8080/tcp
EXPOSE 8080/udp


# nlp module 
COPY ./nlp /code/nlp
COPY ./nlp_router.py /code/nlp_router.py

# firebase 
# NOW TOKEN MUST BE IN PLACE BEFORE RUNNING PROGRAM
COPY ./firebase_key.json /code/firebase_key.json
COPY ./firebase /code/firebase



CMD ["python", "nlp_router.py"]

ENV PYTHONPATH=./
