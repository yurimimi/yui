FROM python:3.8-slim

RUN useradd --create-home --shell /bin/bash app_user
WORKDIR /home/app_user
# COPY requirements.txt ./
RUN apt-get update && apt-get install -y git
RUN python -m pip install git+https://github.com/yurimimi/yui
USER app_user
COPY . .
CMD ["bash"]
