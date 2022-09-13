FROM python:3.11.0rc2-slim

WORKDIR /app

RUN apt update \
    && apt install -y git \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

EXPOSE 8000
CMD python -m uvicorn gitserver:app --host 0.0.0.0 --port 8000
