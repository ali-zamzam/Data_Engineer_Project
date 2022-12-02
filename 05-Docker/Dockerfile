FROM debian:latest

WORKDIR /fastapi-app

RUN apt-get update && apt-get install python3-pip -y

COPY ./requirements.txt /fastapi-app/requirements.txt

COPY ./model.pkl /fastapi-app/

COPY ./main.py /fastapi-app/

RUN pip install --no-cache-dir --upgrade -r /fastapi-app/requirements.txt


CMD ["uvicorn", "main:app","--host", "0.0.0.0", "--port", "8000"]