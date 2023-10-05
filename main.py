# TODO: use to seed the project
# - https://github.com/tiangolo/full-stack-fastapi-postgresql
# - https://fastapi.tiangolo.com/project-generation/
# TODO: add tests

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

import models
from api import get_instances_data
from analytics import store_instances_data, get_ranked_m5_instances
from database import engine, get_database

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# TODO: use Rocketry to execute every 30 min
# @repeat_every(seconds=60 * 30)  # 30 min
@app.get("/get-instances")
async def get_instances(database: Session = Depends(get_database)):
    """
    Calls AWS API to retrieve instance offering data, persist data into the database,
    and returns all the retrieved data as JSON

    Sample request http://localhost:8000/get-instances
    :param database: Injected dependency
    :return: a list of retrieved instances from AWS
    """
    instance_data_list = get_instances_data()
    store_instances_data(database, instance_data_list)
    return instance_data_list


@app.get("/get-ranked-instances")
async def rank_instances(instance_date: str, database: Session = Depends(get_database)):
    """
    Sample request http://localhost:8000/get-ranked-instances?instance_date=2023-10-04

    :param instance_date: specific date e.g. '2023-10-04'
    :param database: Injected dependency
    :return: a list or ranked m5 instance starting with most liquid
    """
    results = get_ranked_m5_instances(database, instance_date)
    return {"sorted_results": results}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
