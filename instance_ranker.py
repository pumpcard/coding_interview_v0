import boto3
from aws_instances import AwsInstanceTypes
from queue import PriorityQueue
from ec2_response import InstanceOfferingResponse
class InstanceRanker():

    def hello_world() -> str:
        return "hello world"
    
    def __init__(self) -> None:
        self.create_client()

    def create_client(self) -> None:
        try:
            self.client = boto3.client('ec2')
        except Exception as e:
            raise Exception(str(e))
    
    def get_reserved_instance_offerings(self, instance_type: str):
        response = self.client.describe_reserved_instances_offerings(
            InstanceType=instance_type,
            MaxResults=10
        )
        return response
    
    def parse_response(self, instance_offerings):
        parsed_offerings = []
        for instance_offering in instance_offerings:
            offering = InstanceOfferingResponse(instance_offering)
            parsed_offerings.append(offering)
        return parsed_offerings

    def rank_all_instances(self):
        all_instances = self.get_all_instances()
        PriorityQueue()
        return all_instances
    
    ###
    # For the sake of speed, im disabling the next token
    # The way i would handle this pagination issue would be load the ranks as a batch process
    # and then keep those ranks recorded in our own db
    ###
    def get_all_instances(self):
        all_instances = []
        # next_token = ''
        for aws_instance_type in AwsInstanceTypes:
            # while next_token is not None:
            response = self.get_reserved_instance_offerings(instance_type=aws_instance_type.value)
            all_instances.extend(self.parse_response(response['ReservedInstancesOfferings']))
                # next_token = response['NextToken']

        return all_instances

    


    
