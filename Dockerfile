FROM python:3.10-slim

WORKDIR /code
 
COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip
# Install core dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]