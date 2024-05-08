# Use an official Python image as a base
FROM python:3.10-slim-bullseye

# Set environment variables
ENV HOST=0.0.0.0
ENV LISTEN_PORT 8080

# Install dependencies
RUN apt-get update && apt-get install -y git
RUN pip install --no-cache-dir --upgrade playwright streamlit

# Copy requirements file
COPY ./requirements.txt /app/requirements.txt

# Install requirements
RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["playwright", "install"]

# Create a new directory for the app
WORKDIR /app

# Copy the app code
COPY ./ /app/

# Expose the port
EXPOSE 8080

# Run the command to start the Streamlit app
CMD ["streamlit", "run", "demo_app/main.py", "--server.port", "8080"]