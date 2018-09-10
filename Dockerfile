# Dockerfile for CAB432 Assessment (individual project)
# Student Name: Jaimyn Mayer (n9749331)

# Our base image is Ubuntu 16.04
FROM ubuntu:16.04

# Pls don't spam my email
MAINTAINER Jaimyn Mayer (hello@jaimyn.com.au)

# Update the repos and install the basics
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install --upgrade pip

# Copy our codes and stuff
ADD /app /app

# Set our default working directory
WORKDIR /app

# Install the requirements with pip
RUN pip3 install -r requirements.txt



# Expose our port and start our app
EXPOSE 8000
ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8000", "--module", "backend.app:app", "--processes", "1", "--threads", "8"]
