from instance_ranker import InstanceRanker
from fastapi import FastAPI
from starlette.responses import RedirectResponse

app = FastAPI()

instance_ranker = InstanceRanker()

@app.on_event("startup")
async def startup_event():
    instance_ranker.get_all_instances()
    instance_ranker.rank_all_instances()

@app.get("/ec2InstanceRanker")
async def get_ranked_ec2_instances(page_num: int = 0, page_size:int = 10):
    page = instance_ranker.get_ranked_instances_by_page(page_num=page_num, page_size=page_size)
    
    return page