from recurring_charge import RecurringCharge

class InstanceOfferingResponse():

    duration: float
    fixed_price: float
    instance_type: str
    product_description: str
    reserved_instance_offering_id: str
    usage_price: float
    currency_code: str
    instance_tenancy: str
    marketplace: bool
    offering_class: str
    offering_type: str
    pricing_details: list
    recurring_charges: list[RecurringCharge]
    scope: str

    def __init__(self, instance_response_dict) -> None:
        self.duration = instance_response_dict['Duration']
        self.fixed_price = instance_response_dict['FixedPrice']
        self.instance_type = instance_response_dict['InstanceType']
        self.product_description = instance_response_dict['ProductDescription']
        self.reserved_instance_offering_id = instance_response_dict['ReservedInstancesOfferingId']
        self.usage_price = instance_response_dict['UsagePrice']
        self.currency_code = instance_response_dict['CurrencyCode']
        self.instance_tenancy = instance_response_dict['InstanceTenancy']
        self.marketplace = instance_response_dict['Marketplace']
        self.offering_class = instance_response_dict['OfferingClass']
        self.offering_type = instance_response_dict['OfferingType']
        self.pricing_details = instance_response_dict['PricingDetails']
        self.scope = instance_response_dict['Scope']
        self.unpackRecurringCharges(instance_response_dict)

    def unpackRecurringCharges(self, instance_response_dict):
        recurring_charges_response = instance_response_dict['RecurringCharges']
        self.recurring_charges = []
        for recurring_charge in recurring_charges_response:
            self.recurring_charges.append(RecurringCharge(recurring_charge))