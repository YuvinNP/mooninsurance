FROM python:3.9.0

WORKDIR /mooninsurance/integration

COPY . .

RUN apt-get update \
  && apt-get install unixodbc -y \
  && apt-get install unixodbc-dev -y

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose the port the service runs on
EXPOSE 5000

# Define the command to run the service
CMD ["python", "integration_app.py"]