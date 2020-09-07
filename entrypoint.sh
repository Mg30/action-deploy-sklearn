# /bin/sh

cp validation.py app/backend/api/app
cd app/backend/api
sls plugin install -n serverless-python-requirements
sls deploy > sls.txt
cd $GITHUB_WORKSPACE
python3 app/endpoint.py app/backend/api/sls.txt
endpoint=$(cat app/backend/api/sls.txt)
echo "::set-output name=endpoint::$endpoint"