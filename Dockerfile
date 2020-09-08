FROM python:3.7


RUN apt update && apt install -y sudo

RUN apt-get update && apt-get install -y \
        curl \
        zip  \
        unzip
RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
RUN sudo apt -y install nodejs   

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
                && unzip awscliv2.zip \
                && ./aws/install

RUN npm install -g serverless@1.72.0
COPY entrypoint.sh .
COPY app/ /app/
ENTRYPOINT [ "/bin/sh","/entrypoint.sh" ]
