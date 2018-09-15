# Dockerfile for CAB432 Assessment (individual project)
# Student Name: Jaimyn Mayer (n9749331)

# Our base image is Ubuntu 18.04
FROM ubuntu:16.04
MAINTAINER Jaimyn Mayer (hello@jaimyn.com.au)

# Update the repos and install the basics
RUN apt-get update
RUN apt-get install -y \
    python3 \
    python3-pip \
    cron \
    wget \
    vim
    # vim lyfe

RUN pip3 install --upgrade pip

# Copy our codes and stuff
ADD /app /app

# Set our default working directory
WORKDIR /app/backend

# Install the requirements with pip
RUN pip3 install -r requirements.txt

# copy our cron config
RUN cp cab432-cron /etc/cron.d/cab432-cron
RUN chmod 0644 /etc/cron.d/cab432-cron
RUN crontab /etc/cron.d/cab432-cron
RUN touch /var/log/cron.log

# Expose our port and start our app
EXPOSE 8000
CMD /usr/sbin/cron -f & && uwsgi --http 0.0.0.0:8000 --module app:app --processes 1 --threads 8
