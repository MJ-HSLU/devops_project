# Start from a base-image containing Python 3.11 ("slim" is a minimal OS version)
FROM python:3.11-slim

# Defines the working directory to be "/code"
WORKDIR /code

# Copies the requirements.txt into the container
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all source code into the container's /code directory
COPY . /code

# Extend "PYTHONPATH" to ensure modules can be imported
ENV PYTHONPATH="/code"

# Expose port 8080 for external access
EXPOSE 8080

# Start the FastAPI application using uvicorn from main.py
CMD ["uvicorn", "server.py.main:app", "--host", "0.0.0.0", "--port", "8080"]
