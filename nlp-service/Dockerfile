FROM python:3.9

WORKDIR /code


# install requirements
COPY ./requirements.txt /code
RUN pip install pip --upgrade
# RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install -r /code/requirements.txt

EXPOSE 8080/tcp
EXPOSE 8080/udp

# nlp module 
COPY ./nlp /code/nlp
COPY ./nlp_router.py /code/nlp_router.py
# Initialize NLP
RUN python ./nlp/similarity_providers.py

# firebase 
# NOW TOKEN MUST BE IN PLACE BEFORE RUNNING PROGRAM
COPY ./firebase_key.json /code/firebase_key.json
COPY ./firebase /code/firebase



CMD ["python", "nlp_router.py"]

ENV PYTHONPATH=./
