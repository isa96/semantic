# Use the official Python image as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy only the 'requirements.txt' file into the container's working directory
COPY src/requirements.txt .

# Install required packages from 'requirements.txt'
RUN pip install -r requirements.txt

# Copy the rest of the content of the 'src' directory into the container's working directory
COPY src/ .

# Expose the port on which the FastAPI application will run
EXPOSE 8000

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]