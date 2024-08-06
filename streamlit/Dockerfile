FROM python:3.9-slim

WORKDIR /app

# Copy the application file
COPY app.py app.py
COPY .streamlit/secrets.toml .streamlit/secrets.toml
COPY documents.json documents.json

# Install any required packages
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt


HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

CMD ["streamlit", "run", "app.py"]