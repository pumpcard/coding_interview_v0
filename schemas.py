from typing import Optional, List

from pydantic import BaseModel


class PricingDetails(BaseModel):
    Count: int
    Price: float

    def to_dict(self):
        return {
            "count": self.Count,
            "price": self.Price
        }


class RecurringCharge(BaseModel):
    Amount: float
    Frequency: str

    def to_dict(self):
        return {
            "amount": self.Amount,
            "frequency": self.Frequency
        }


class InstanceData(BaseModel):
    Duration: int
    FixedPrice: float
    InstanceType: str
    ProductDescription: str
    ReservedInstancesOfferingId: str
    UsagePrice: float
    CurrencyCode: str
    InstanceTenancy: str
    Marketplace: bool
    OfferingClass: str
    OfferingType: str
    PricingDetails: Optional[List[PricingDetails]]
    RecurringCharges: Optional[List[RecurringCharge]]
    Scope: str


class AnalyticsRequestParams(BaseModel):
    instance_type: str
    specific_date: str


class InstancesVolumeAnalyticsResult(BaseModel):
    params: AnalyticsRequestParams
    min_count: int
    max_count: int
    avg_count: float
