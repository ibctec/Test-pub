FROM python:3.12

# Install Poetry
RUN pip install poetry

# Verify Poetry version
RUN poetry --version

# Set the working directory
WORKDIR /app

RUN pwd
RUN ls -al /app

# Copy and install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
RUN ls -al /app

# Copy application code
COPY . .
EXPOSE 8000:8000

# Command to run the application (change as needed)
CMD ["poetry", "run", "uvicorn", "emp.main:app", "--host", "0.0.0.0", "--port", "8000"]
