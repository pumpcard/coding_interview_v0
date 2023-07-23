import boto3
import json

ec2 = boto3.client("ec2", region_name="us-east-1")

offerings = []
offerings_paginator = ec2.get_paginator("describe_reserved_instances_offerings")
offerings_iterator = offerings_paginator.paginate(
    Filters=[{"Name": "instance-type", "Values": ["a1.2xlarge"]}], MaxResults=100
)


def write_offering(offering):
    print(json.dumps(offering))


#
# Note: it appears NextToken is always present, so it cannot be relied upon for end-of-set detection.
# It also appears that the first request to RIO will have an empty RIO set, but subsequent calls with NextTokens will have the RIO objects.
#
saw_empty = False
for offering_resp in offerings_iterator:
    returned_offerings = offering_resp["ReservedInstancesOfferings"]
    if len(returned_offerings) == 0:
        if saw_empty:
            break
        else:
            saw_empty = True

    for offering in returned_offerings:
        write_offering(offering)
