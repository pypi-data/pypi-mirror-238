class Transaction:
    def __init__(self, amount, card_reference, created_at, kind, merchant, reference, status, slug) -> None:
        self.amount = amount
        self.card_reference = card_reference
        self.created_at = created_at
        self.kind = kind
        self.merchant = merchant
        self.reference = reference
        self.status = status
        self.slug = slug
