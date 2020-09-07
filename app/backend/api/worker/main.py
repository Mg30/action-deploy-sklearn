try:
  import unzip_requirements
except ImportError:
  pass
import boto3
import os
import pickle
import json
import pandas as pd

QUEUE_TABLE = os.environ["QUEUE_TABLE"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
MODEL_KEY = os.environ["MODEL_KEY"]

dynamodb = boto3.client("dynamodb")
s3 = boto3.resource("s3")
model = pickle.loads(s3.Bucket(BUCKET_NAME).Object(MODEL_KEY).get()["Body"].read())


def handler(event, context):
    for record in event["Records"]:
        prediction_id = record["messageId"]
        payload = json.loads(record["body"])
        df = pd.DataFrame(payload)
        status = ""
        body = None
        try:
            body = str(model.predict(df)[0])
            status = "COMPLETE"
        except Exception as e:
            status = f"ERROR:{e}"
        finally:
            dynamodb.put_item(
                TableName=QUEUE_TABLE,
                Item={
                    "prediction_id": {"S": prediction_id},
                    "status": {"S": status},
                    "body": {"N": body},
                },
            )
