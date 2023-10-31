class Dispute:
    def __init__(self, explanation, reason, reference, status, transaction_reference) -> None:
        self.explanation = explanation
        self.reason = reason
        self.reference = reference
        self.status = status
        self.transaction_reference = transaction_reference
