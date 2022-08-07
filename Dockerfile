FROM python:3.10.4

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /random_words

COPY . .
RUN pip install --no-cache-dir -r requirements/prod.txt && \
    rm -rf requirements