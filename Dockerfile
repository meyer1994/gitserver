FROM python:slim

COPY . /app

WORKDIR /app

RUN apt update && apt install -y git
RUN pip install -r requirements.txt

EXPOSE 8000

CMD python -m uvicorn app:app --host 0.0.0.0 --port 8000
