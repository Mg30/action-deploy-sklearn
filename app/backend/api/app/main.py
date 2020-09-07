try:
    import unzip_requirements
except ImportError:
    pass

try:
    import uvicorn
except ImportError:
    pass

from validation import PredictionData
import boto3
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from typing import List
import json

SQS_URL = os.getenv("SQS_URL")
QUEUE_TABLE = os.environ["QUEUE_TABLE"]
sqs = boto3.client("sqs")
dynamodb = boto3.client("dynamodb")


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"],
)
handler = Mangum(app)


@app.get("/")
def hello_world():
    return {"hello": "world"}


@app.post("/api/predict")
async def predict(data: PredictionData):
    formated_data = {}
    for key, value in data.dict().items():
        formated_data[key] = [value]

    json_data = json.dumps(formated_data)
    message = sqs.send_message(QueueUrl=SQS_URL, MessageBody=json_data)
    prediction_id = message["MessageId"]
    dynamodb.put_item(
        TableName=QUEUE_TABLE,
        Item={"prediction_id": {"S": prediction_id}, "status": {"S": "PENDING"}},
    )
    return {"prediction_id": prediction_id}


@app.get("/api/predict/{prediction_id}")
def get_message_status(prediction_id: str):
    resp = dynamodb.get_item(
        TableName=QUEUE_TABLE, Key={"prediction_id": {"S": prediction_id}}
    )
    item = resp.get("Item")
    if item is None:
        raise HTTPException(status_code=404, detail="prediction not found")
    body = item.get("body")
    if body:
        body = body.get("N")
    return {
        "prediction_id": item.get("prediction_id").get("S"),
        "status": item.get("status").get("S"),
        "body": body,
    }



# To run locally
if __name__ == "__main__":
    uvicorn.run(app)
