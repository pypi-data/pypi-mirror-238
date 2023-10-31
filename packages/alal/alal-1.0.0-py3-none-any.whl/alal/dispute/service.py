from alal.base import Alal, pagination_filter
from .model import Dispute


class DisputeService(Alal):
    """
        Dispute class
    """

    def __generate_dispute_object(self, data):
        return Dispute(
            explanation=data["explanation"],
            reason=data["reason"],
            reference=data["reference"],
            status=data["status"],
            transaction_reference=data["transaction_reference"]
        )

    def create_dispute(self, body):
        """
            create dispute on alal platform 
            body = {
                "explanation" = "No real explanation even now", 
                "reason" = "duplicate", 
                "transaction_reference" = "962b954d-bbd3-4b03-8a70"
            }

            POST request 
        """

        required_data = ["explanation", "reason", "transaction_reference"]
        self.check_required_data(required_data, body)

        response = self.send_request("POST", "disputes/create", json=body)
        return self.__generate_dispute_object(data=response.get("data", {}).get("dispute"))

    def list_dispute(self, **kwargs):
        """
            list all disputes
            GET request
        """
        url_params = None
        if kwargs != {}:
            url_params = pagination_filter(**kwargs)
        response = self.send_request("GET", f"disputes?{url_params}")
        data = response["data"]
        return [self.__generate_dispute_object(dispute_data) for dispute_data in data]

    def show_dispute(self, reference):
        """
            show disputes details
            GET request
        """
        response = self.send_request("GET", f"disputes/{reference}")
        return self.__generate_dispute_object(data=response.get("data", {}).get("dispute"))

    def update_dispute(self, body, reference):
        """
            update dispute on alal platform 
            body = {
                "explanation" = "No real explanation even now", 
                "reason" = "fraudulent", 
                "transaction_reference" = "962b954d-bbd3-4b03-8a12"
            }

            POST request 
        """

        required_data = ["explanation", "reason", "transaction_reference"]
        self.check_required_data(required_data, body)

        response = self.send_request(
            "POST", f"disputes/update/{reference}", json=body)
        return self.__generate_dispute_object(data=response.get("data", {}).get("dispute"))
