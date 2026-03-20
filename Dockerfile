# Use the official Python base image
FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Set the working directory inside the container
WORKDIR /code

# Copy the requirements file to the working directory
COPY requirements.txt /code/requirements.txt

# Install the Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code to the working directory
COPY . /code

# Expose the port on which the application will run
EXPOSE 8001

CMD ["uvicorn", "app.main:app","--reload", "--host", "0.0.0.0", "--port", "8001"]


