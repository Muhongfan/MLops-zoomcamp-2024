FROM python:3.10.13

# Upgrade pip and install pipenv
RUN pip install -U pip
RUN pip install pipenv

# Set the working directory inside the container
WORKDIR /app
RUN mkdir -p /app/downlads

# Copy Pipfile and Pipfile.lock to the working directory
COPY ["Pipfile", "Pipfile.lock", "./"]

# Install dependencies specified in Pipfile
RUN pipenv install --system --deploy

# Copy application files and model
COPY predict.py ./

# Expose the port that the application will run on
EXPOSE 9696

# Define the command to run the application
ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "--chdir=/app/", "predict:app" ]