from unittest import TestCase

from aws_instances import AwsInstanceTypes
from instance_ranker import InstanceRanker

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
        ranker = InstanceRanker()
        instances = ranker.get_all_instances()
        self.assertEqual(len(instances), 10 * (len(AwsInstanceTypes) - 1))


        