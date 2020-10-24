FROM python:3.8.5

WORKDIR /code
COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["/code/entrypoint.sh"]