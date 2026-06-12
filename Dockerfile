FROM python:3.12-slim

WORKDIR /app

RUN python -m pip install --upgrade pip

# Copy only backend files needed to run the FastAPI app.
COPY backend/ ./backend/
COPY backend/requirements.txt ./backend/requirements.txt

RUN pip install --no-cache-dir -r backend/requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
