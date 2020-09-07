FROM node:lts


RUN apt-get update && apt-get install -y \
        curl \
        zip  \
        unzip \
        python3-pip

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
                && unzip awscliv2.zip \
                && ./aws/install

RUN sudo npm install -g serverless  \
    sls plugin install -n serverless-python-requirements
