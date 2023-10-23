import boto3
from aws_instances import AwsInstanceTypes
from queue import PriorityQueue
from ec2_response import InstanceOfferingResponse
from database.database_connection import RankerDB

class InstanceRanker():

    def hello_world() -> str:
        return "hello world"
    
    def __init__(self, db: RankerDB = None) -> None:
        self.create_client()
        self.db = RankerDB() if db == None else db

    def create_client(self) -> None:
        try:
            self.client = boto3.client('ec2')
        except Exception as e:
            raise Exception(str(e))
    
    def get_reserved_instance_offerings(self, instance_type: str):
        response = self.client.describe_reserved_instances_offerings(
            InstanceType=instance_type
        )
        return response
    
    def parse_response(self, instance_offerings):
        parsed_offerings = []
        for instance_offering in instance_offerings:
            offering = InstanceOfferingResponse(instance_offering)
            parsed_offerings.append(offering)
        return parsed_offerings

    def rank_all_instances(self):
        instance_ranker = PriorityQueue()

        for id in self.db.all_instances:
            instance = self.db.all_instances[id]
            price = instance.fixed_price
            for recurring_charge in instance.recurring_charges:
                if recurring_charge.frequency == 'HOURLY':
                    price += recurring_charge.amount * 24
                if recurring_charge.frequency == 'DAILY':
                    price += recurring_charge.amount
            instance_ranker.put(id, price)
        
        rank = 1
        while instance_ranker.qsize() > 0:
            instance_id = instance_ranker.get()
            self.db.instance_ranks[rank] = instance_id
            rank += 1


    ###
    # For the sake of speed, im disabling the next token
    # The way i would handle this pagination issue would be load the ranks as a batch process
    # and then keep those ranks recorded in our own db
    ###
    def get_all_instances(self):
        all_instances = []
        for aws_instance_type in AwsInstanceTypes:
            response = self.get_reserved_instance_offerings(instance_type=aws_instance_type.value)
            all_instances.extend(self.parse_response(response['ReservedInstancesOfferings']))
            next_token = response['NextToken']
            # while next_token is not None:
            #     response = self.get_reserved_instance_offerings(instance_type=aws_instance_type.value)
            #     all_instances.extend(self.parse_response(response['ReservedInstancesOfferings']))
            #     next_token = response['NextToken']
        
        self.add_to_db(all_instances)
    
    def add_to_db(self, all_instances: list[InstanceOfferingResponse]):
        for instance in all_instances:
            self.db.all_instances[instance.reserved_instance_offering_id] = instance

    def get_ranked_instances_by_page(self, page_num = 0, page_size = 10):
        page = {}
        all_instances = self.db.all_instances
        id_by_ranks = self.db.instance_ranks
        min_rank = 1 + (page_size * page_num)
        max_rank = page_size + (page_size * page_num)
        for rank in range(min_rank, max_rank + 1):
            if rank <= self.db.get_max_rank():
                page[rank] = all_instances[id_by_ranks[rank]]

        return page
    

    


    
