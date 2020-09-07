FROM node:lts

COPY entrypoint.sh .
COPY app/ /app/

RUN apt-get update && apt-get install -y \
        curl \
        zip  \
        unzip \
        python3-pip

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
                && unzip awscliv2.zip \
                && ./aws/install

RUN npm install -g serverless
ENTRYPOINT [ "./entrypoint.sh" ]
