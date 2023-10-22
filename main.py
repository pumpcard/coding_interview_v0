from instance_ranker import InstanceRanker
from fastapi import FastAPI

app = FastAPI()
class EntryPoint():

    @app.get("/ec2InstanceRanker")
    async def get_ranked_ec2_instances():
        instance_ranker = InstanceRanker()
        instances = instance_ranker.get_reserved_instance_offerings()
        return {"msg" : instances}