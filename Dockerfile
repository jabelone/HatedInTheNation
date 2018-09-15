# Dockerfile for CAB432 Assessment (individual project)
# Student Name: Jaimyn Mayer (n9749331)

# Our base image is Ubuntu 16.04
FROM python:3.7-slim
MAINTAINER Jaimyn Mayer (hello@jaimyn.com.au)

# Update the repos and install the basics
RUN apt-get update
RUN apt-get install -y \
    cron \
    wget \
    vim \
    build-essential
    # vim lyfe

RUN pip3 install --upgrade pip

# Copy our codes and stuff
ADD /app /app

# Set our default working directory
WORKDIR /app/backend

# copy our cron config
RUN cp cab432-cron /etc/cron.d/cab432-cron
RUN chmod 0644 /etc/cron.d/cab432-cron
RUN crontab /etc/cron.d/cab432-cron
RUN touch /var/log/cron.log

# start the cron daemon on container startup
CMD cron && tail -f /var/log/cron.log

# Install the requirements with pip
RUN pip3 install -r requirements.txt

# Expose our port and start our app
EXPOSE 8000
CMD /usr/sbin/cron -f
ENTRYPOINT ["uwsgi", "--http", "0.0.0.0:8000", "--module", "app:app", "--processes", "1", "--threads", "8"]
