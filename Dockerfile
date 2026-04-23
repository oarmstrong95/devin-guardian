FROM python:3.12-slim

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY src/ /app/src/

WORKDIR /app
CMD ["python", "-m", "src"]
