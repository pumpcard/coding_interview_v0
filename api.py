import boto3
from fastapi import HTTPException
from sqlalchemy import String


# Gets instances' data from AWS and stores in the database
from schemas import InstanceData

PARAM_RESERVED_INSTANCES_OFFERINGS = 'ReservedInstancesOfferings'


def get_instances_data(region: String = 'us-east-2') -> [InstanceData]:
    """
    Uses AWS API to retrieve the reserved instances offering
    :param region: AWS region, defaults to `us-east-2`
    :return: a list of InstanceData objects
    """
    try:
        ec2_client = boto3.client(
            'ec2',
            region_name=region)

        # Fetch reserved instances from AWS
        # TODO: add fetching all the pages
        reserved_instances = ec2_client.describe_reserved_instances_offerings(
            InstanceType='m5.large',
            ProductDescription='Linux/UNIX',
            OfferingType='All Upfront' #'Heavy Utilization'|'Medium Utilization'|'Light Utilization'|'No Upfront'|'Partial Upfront'|'All Upfront'
        )

        instance_data_list = []

        for instance in reserved_instances[PARAM_RESERVED_INSTANCES_OFFERINGS]:
            instance_data = InstanceData(**instance)
            instance_data_list.append(instance_data)

        return instance_data_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))