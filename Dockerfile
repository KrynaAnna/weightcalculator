FROM python:3.11.3-slim-buster

# Create a working directory inside the container
WORKDIR /weightcalculator

# Copy all the files from the current directory into the container's working directory
COPY . .

# Install the Python dependencies
RUN pip install -r requirements.txt

# Set the Flask application entry point
ENV FLASK_APP=main.py

# Expose the port that the Flask app will be listening on
EXPOSE 80

# Set the command to run your Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
