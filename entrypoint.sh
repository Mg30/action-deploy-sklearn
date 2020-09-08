export SERVICE_NAME=$INPUT_SERVICE_NAME
export STAGE= $INPUT_SERVICE_NAME
export AWS_DEFAULT_REGION=$INPUT_AWS_DEFAULT_REGION
export AWS_S3_BUCKETNAME=$INPUT_AWS_S3_BUCKETNAME
export MODEL_KEY=$INPUT_MODEL_KEY
export MODEL_VERSION= $INPUT_MODEL_VERSION

cp validation.py /app/backend/api/app
cd /app/backend/api
sls plugin install -n serverless-python-requirements
sls deploy > sls.txt
cd $GITHUB_WORKSPACE
python3 /app/endpoint.py /app/backend/api/sls.txt
endpoint=$(cat /app/backend/api/sls.txt)
echo "::set-output name=endpoint::$endpoint"