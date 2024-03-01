FROM python:3.12.2-bullseye

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ENV FLASK_APP=flaskr
ENV PYTHON_PATH=flaskr

# Run the application
# RUN flask --app flaskr/app.py run --debug --host="0.0.0.0"