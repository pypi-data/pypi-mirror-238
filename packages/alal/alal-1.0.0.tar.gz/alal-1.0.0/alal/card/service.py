from alal.base import Alal, pagination_filter
from .model import Card


class CardService(Alal):
    """
        Card class
    """

    def __generate_card_object(self, data):
        return Card(
            balance=data["balance"],
            card_type=data["card_type"],
            card_brand=data["card_brand"],
            last_four=data["last_four"],
            reference=data["reference"],
            card_user_reference=data["card_user_reference"],
            status=data["status"],
            created_at=data["created_at"]
        )

    def create_card(self, body: dict):
        """
            create card on alal platform
            body = {
                "card_brand": "visa",
                "card_type": "virtual",
                "card_user_reference": "d282e4a6-1fb6-4827-a6ae-a780263287d7",
            }

            POST request 
        """
        required_data = ["card_type", "card_brand", "card_user_reference"]
        self.check_required_data(required_data, body)

        response = self.send_request("POST", "cards/create", json=body)
        return self.__generate_card_object(data=response.get("data", {}).get("card"))

    def list_card(self, **kwargs):
        """
            list all cards 
            GET request
        """
        url_params = None
        if kwargs != {}:
            url_params = pagination_filter(**kwargs)
        response = self.send_request("GET", f"cards?{url_params}")
        data = response["data"]
        return [self.__generate_card_object(card_data) for card_data in data]

    def show_card(self, reference):
        """
            show card details
            GET request
        """
        response = self.send_request("GET", f"cards/{reference}")
        return self.__generate_card_object(data=response.get("data", {}).get("card"))

    def freeze_card(self, reference):
        """
            freeze card
             body = {
                reference = "d282e4a6-1fb6-4827-a6ae-a780263287d7"
            }
            POST request
        """
        body = {
            "reference": reference
        }

        response = self.send_request("POST", "cards/freeze", json=body)
        return self.__generate_card_object(data=response.get("data", {}).get("card"))

    def unfreeze_card(self, reference):
        """
            unfreeze card
             body = {
                reference = "d282e4a6-1fb6-4827-a6ae-a780263287d7"
            }
            POST request
        """
        body = {
            "reference": reference
        }

        response = self.send_request("POST", "cards/unfreeze", json=body)
        return self.__generate_card_object(data=response.get("data", {}).get("card"))

    def link_card(self, body):
        """
            unfreeze card
             body = {
                reference = "d282e4a6-1fb6-4827-a6ae-a780263287d7"
                card_user_reference = "577f7a27-0749-4c7c-89a3-bcedca3452e9"
            }
            POST request
        """
        required_data = ["reference", "card_user_reference"]
        self.check_required_data(required_data, body)

        response = self.send_request("POST", "cards/link", json=body)
        return self.__generate_card_object(data=response.get("data", {}).get("card"))

    def get_access_token(self, body):
        """
            create card access token 
            body = {
                css_url = "style.css",
                reference = "d282e4a6-1fb6-4827-a6ae-a780263287d7"
            }
            POST request
        """
        required_data = ["reference"]
        self.check_required_data(required_data, body)

        response = self.send_request(
            "POST", "cards/auth/access_token", json=body)
        return response.get("data")
