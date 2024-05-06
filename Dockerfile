FROM python:3.11.9

RUN python -m pip install --upgrade pip

WORKDIR /cloud

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN cd app

CMD [ "uvicorn", "main:app" ]



