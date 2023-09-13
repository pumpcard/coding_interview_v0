# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import boto3

# inits
app = FastAPI()

DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# db stuff
class Instance(Base):
    __tablename__ = "instances"
    id = Column(Integer, primary_key=True, index=True)
    instance_type = Column(String, index=True)
    volume = Column(Integer)
    price = Column(Float)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# services
def fetch_instance_offerings():
    ec2 = boto3.client('ec2')
    offerings = ec2.describe_reserved_instances_offerings(
        InstanceType='m5.large',
        ProductDescription='Linux/UNIX',
        OfferingType='All Upfront'
    )
    return offerings['ReservedInstancesOfferings']

def store_instance_data(session: Session, instance_type: str, volume: int, price: float):
    instance = Instance(instance_type=instance_type, volume=volume, price=price)
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance.id

# http endpoints | APIs
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/fetch-aws-data/")
def fetch_and_store_aws_data(db: Session = Depends(get_db)):
    offerings = fetch_instance_offerings()
    for offering in offerings:
        store_instance_data(db, offering['InstanceType'], offering['InstanceCount'], offering['FixedPrice'])
    return {"status": "data fetched and stored"}

@app.get("/liquidity/{instance_type}")
def get_liquidity(instance_type: str, db: Session = Depends(get_db)):
    instance = db.query(Instance).filter(Instance.instance_type == instance_type).first()
    if instance:
        liquidity_rank = instance.volume
        return {"instance_type": instance.instance_type, "liquidity_rank": liquidity_rank}
    raise HTTPException(status_code=404, detail="Instance type not found")
