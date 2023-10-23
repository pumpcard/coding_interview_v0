from unittest import TestCase

from aws_instances import AwsInstanceTypes
from instance_ranker import InstanceRanker
from database.database_connection import RankerDB
from ec2_response import InstanceOfferingResponse

class InstanceRankerTests(TestCase):

    def test_passes(self):
        self.assertTrue(True)

    def test_empty_list(self):
        ranker = InstanceRanker()
        instances = ranker.get_reserved_instance_offerings(instance_type=AwsInstanceTypes.A1MEDIUM.value)['ReservedInstancesOfferings']
        self.assertEqual(len(instances), 0)
    
    def test_one_page_returned(self):
        ranker = InstanceRanker()
        instances = ranker.get_reserved_instance_offerings(instance_type=AwsInstanceTypes.M1SMALL.value)['ReservedInstancesOfferings']
        self.assertEqual(len(instances), 10)

    def test_all_pages_returned_of_all_type(self):
        db = RankerDB()
        self.generate_instances(db=db, size = 5)
        
        ranker = InstanceRanker(db=db)
        ranker.rank_all_instances()
        
        page = ranker.get_ranked_instances_by_page(page_num=0, page_size=10)
        self.assertEqual(len(page.keys()), 5)


    def generate_instances(self, db: RankerDB, size: int = 1):
        id = 0
        while id < size:

            offering_dict =  {
                "Duration": 31536000,
                "FixedPrice": 257.0 + id,
                "InstanceType": "m1.small",
                "ProductDescription": "Linux/UNIX",
                "ReservedInstancesOfferingId": str(id),
                "UsagePrice": 0.0,
                "CurrencyCode": "USD",
                "InstanceTenancy": "default",
                "Marketplace": False,
                "OfferingClass": "standard",
                "OfferingType": "All Upfront",
                "PricingDetails": [],
                "RecurringCharges": [
                    {
                        "Amount": 0.0,
                        "Frequency": "Hourly"
                    }
                ],
                "Scope": "Region"
            }
            instance = InstanceOfferingResponse(offering_dict)
            db.all_instances[str(id)] = instance
            id += 1
        