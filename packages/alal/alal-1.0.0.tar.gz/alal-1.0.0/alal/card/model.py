class Card:
    def __init__(self, balance, card_brand, card_type, last_four, reference, card_user_reference, status, created_at) -> None:
        self.balance = balance
        self.card_brand = card_brand
        self.card_type = card_type
        self.last_four = last_four
        self.reference = reference
        self.card_user_reference = card_user_reference
        self.status = status
        self.created_at = created_at
