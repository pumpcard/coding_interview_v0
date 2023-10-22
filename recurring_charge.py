class RecurringCharge():
    amount: float
    frequency: str

    def __init__(self, charge_response) -> None:
        self.amount = charge_response['Amount']
        self.frequency = charge_response['Frequency']