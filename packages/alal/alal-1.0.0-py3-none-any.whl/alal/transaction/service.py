from alal.base import Alal, pagination_filter
from .model import Transaction


class TransactionService(Alal):
    """
        transaction class
    """

    def __generate_transaction_object(self, data):
        return Transaction(
            amount=data["amount"],
            card_reference=data["card_reference"],
            created_at=data["created_at"],
            kind=data["kind"],
            merchant=data["merchant"],
            reference=data["reference"],
            status=data["status"],
            slug=data["slug"]
        )

    def create_transaction(self, body):
        """
            create card transaction 
            body = {
                "action" = "recharge",
                "amount" = "2000"
                card_reference = "9c54515e-7890-44f9-8cc2-a85b80322b98"
            }
            POST request
        """

        required_data = ["action", "amount", "card_reference"]
        self.check_required_data(required_data, body)

        response = self.send_request("POST", "transactions/create", json=body)
        return self.__generate_transaction_object(data=response.get("data", {}).get("transaction"))

    def list_transaction(self, **kwargs):
        """
            list all card transaction
            GET request
        """
        url_params = None
        if kwargs != {}:
            url_params = pagination_filter(**kwargs)
        response = self.send_request("GET", f"transactions?{url_params}")
        data = response["data"]
        return [self.__generate_transaction_object(transaction_data) for transaction_data in data]

    def show_transaction(self, reference):
        """
            show transaction details
            GET request
        """
        response = self.send_request("GET", f"transactions/{reference}")
        return self.__generate_transaction_object(data=response.get("data", {}).get("transaction"))
