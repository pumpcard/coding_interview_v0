import json
from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, Boolean, JSON, DateTime
from sqlalchemy.ext.hybrid import hybrid_property

from database import Base
from schemas import InstanceData


class InstanceDataORM(Base):
    __tablename__ = 'instances'
    id = Column(Integer, primary_key=True, autoincrement=True)
    _timestamp = Column('timestamp', DateTime)
    duration = Column(Integer)
    fixed_price = Column(Float)
    instance_type = Column(String(100))
    product_description = Column(String(100))
    reserved_instances_offering_id = Column(String(100))
    usage_price = Column(Float)
    currency_code = Column(String(10))
    instance_tenancy = Column(String(20))
    marketplace = Column(Boolean)
    offering_class = Column(String(20))
    offering_type = Column(String(20))
    pricing_details = Column(JSON)
    recurring_charges = Column(JSON)
    scope = Column(String(20))

    # Required to avoid overwriting the DB records with data populated form code
    @hybrid_property
    def timestamp(self):
        # Return the timestamp if it's set, otherwise return None
        return self._timestamp if self._timestamp else None

    @timestamp.setter
    def timestamp(self, value):
        # Set the timestamp only if it's not set already
        if not self._timestamp:
            self._timestamp = value

    @timestamp.expression
    def timestamp(self):
        return self._timestamp

    def from_pydantic(self, instance_data: InstanceData):
        self.duration = instance_data.Duration
        self.fixed_price = instance_data.FixedPrice
        self.instance_type = instance_data.InstanceType
        self.product_description = instance_data.ProductDescription
        self.reserved_instances_offering_id = instance_data.ReservedInstancesOfferingId
        self.usage_price = instance_data.UsagePrice
        self.currency_code = instance_data.CurrencyCode
        self.instance_tenancy = instance_data.InstanceTenancy
        self.marketplace = instance_data.Marketplace
        self.offering_class = instance_data.OfferingClass
        self.offering_type = instance_data.OfferingType
        self.pricing_details = json.dumps([detail.to_dict() for detail in instance_data.PricingDetails])
        self.recurring_charges = json.dumps([charge.to_dict() for charge in instance_data.RecurringCharges])
        self.scope = instance_data.Scope
