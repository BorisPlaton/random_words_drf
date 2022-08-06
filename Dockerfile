FROM python:3.10.4

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /random_words

COPY requirements/prod.txt .
RUN pip install --no-cache-dir -r prod.txt && rm -f prod.txt

COPY . .