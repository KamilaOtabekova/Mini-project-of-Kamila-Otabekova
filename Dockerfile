#Change to your python version.
#If you do not know yours, use in python's terminal:
```
python --version
```
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    && apt-get clean

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

CMD ["python", "app.py"]
