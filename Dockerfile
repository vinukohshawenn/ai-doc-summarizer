# Start with a lightweight Python image
FROM python:3.11-slim

# Copy the official uv binary straight from its official image (the cleanest way)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies using uv
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# Copy all your application code into the container
COPY . .

# Expose the port Uvicorn runs on
EXPOSE 8000

# Initialize the DB and then start the server
CMD ["sh", "-c", "python init_db.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
