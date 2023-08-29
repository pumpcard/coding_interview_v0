from fastapi import FastAPI
import boto3

from db import data
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get_m5_offerings/{instance_type}")
async def get_m5_offerings(instance_type: str):
    client = boto3.client('ec2')

    offerings = 0
    offers_with_prices = 0

    response = client.describe_reserved_instances_offerings(
        InstanceType=instance_type,
    )
    o, p = data.ingest(response)
    offerings += o
    offers_with_prices += p

    next_token = response['NextToken']
    while next_token is not None:
        response = client.describe_reserved_instances_offerings(
            InstanceType=instance_type,
            NextToken=next_token
        )
        o, p = data.ingest(response)
        offerings += o
        offers_with_prices += p

        if 'NextToken' in response:
            next_token = response['NextToken']
        else:
            next_token = None

    return {'offerings': offerings, 'available_prices': offers_with_prices}


@app.get("/rank_m5_offering/{instance_type}")
async def rank_m5_offering(instance_type: str):
    return {"message": 'hello!'}
