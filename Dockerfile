# FROM ubuntu:latest
# USER root
# WORKDIR /app

# ENV DEBIAN_FRONTEND=noninteractive
# ENV TZ=Europe/Berlin
# RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# RUN apt-get update \
#     && apt-get install -y sudo python3-pip python3-dev \
#     && cd /usr/local/bin \
#     && ln -s /usr/bin/python3 python \
#     && pip3 install --upgrade pip 

# RUN adduser --disabled-password --gecos '' docker
# RUN adduser docker sudo
# RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# USER docker

# RUN sudo apt-get update 

# RUN sudo apt-get -qq -y install firefox
# RUN sudo apt-get install firefox-geckodriver

# COPY . /app
# RUN pip install --no-cache-dir -r requirements.txt


# CMD ['python', '/utils/insta_comment_scraper.py']

FROM python:3.10
USER root
WORKDIR /app


COPY . /app
RUN apt-get -y update
RUN pip install --upgrade pip
RUN apt-get install zip -y
RUN apt-get install unzip -y

# Install chromedriver
RUN wget -N https://chromedriver.storage.googleapis.com/109.0.5414.74/chromedriver_linux64.zip -P ~/
RUN unzip ~/chromedriver_linux64.zip -d ~/
RUN rm ~/chromedriver_linux64.zip
RUN mv -f ~/chromedriver /usr/local/bin/chromedriver
RUN chown root:root /usr/local/bin/chromedriver
RUN chmod 0755 /usr/local/bin/chromedriver


# Install chrome broswer
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get -y install google-chrome-stable


RUN pip install -r requirements.txt

CMD ['python', '/utils/insta_comment_scraper.py']
# CMD uvicorn app:app --host 0.0.0.0 