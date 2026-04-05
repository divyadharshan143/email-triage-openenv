FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir gradio pydantic

CMD ["python", "app.py"]