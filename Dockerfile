# Dockerfile for CAB432 Assessment (individual project)
# Student Name: Jaimyn Mayer (n9749331)

# Our base image is Ubuntu 18.04
FROM ubuntu:16.04
MAINTAINER Jaimyn Mayer (hello@jaimyn.com.au)

# Update the repos and install the basics
RUN apt-get update
RUN apt-get install -y \
    apt-utils \
    curl \
    python3 \
    python3-pip \
    vim
    # vim lyfe

# add the node repo and install it, then check version
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash
RUN apt-get update
RUN apt-get install -y nodejs
RUN nodejs -v

# Copy our codes and stuff
ADD /app /app

# Set our default working directory to do node stuff
WORKDIR /app/frontend
RUN npm run build

# Set our default working directory to install python stuff and run flask
WORKDIR /app/backend

# Upgrade pip then install the requirements
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt


# Expose our port and start our app
EXPOSE 8000
CMD uwsgi --http 0.0.0.0:8000 --module app:app --processes 1 --threads 8
