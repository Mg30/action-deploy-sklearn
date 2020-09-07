# /bin/sh

cp validation.py app/backend/api/app
cd app/backend/api
sls deploy > sls.txt
cd $GITHUB_WORKSPACE
python3 app/endpoint.py app/backend/api/sls.txt