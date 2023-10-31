from alal.base import Alal, pagination_filter
from .model import CardUser


class CardUserService(Alal):
    """
        CardUser class
    """

    def __generate_cardUser_object(self, data):
        return CardUser(
            address=data["address"],
            created_at=data["created_at"],
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            id_no=data["id_no"],
            phone=data["phone"],
            reference=data["reference"],
            status=data["status"],
        )

    def create_card_user(self, body):
        """
            create card user on alal platform 
            body = {
                    "address": "rue ng 59 grand ngor",
                    "email": "ndiayendeyengone99@gmail.com",
                    "first_name": "ndeye ngone",
                    "id_no": "20119991010000621",
                    "last_name": "ndiaye",
                    "phone": "774964996", 
                    "id_image": "image.jpeg", 
                    "selfie_image": "selfie.jpeg",
                    "back_id_image": "back.jpeg"
            }
            POST request
        """
        required_data = ["address", "back_id_image", "email", "first_name",
                         "last_name", "id_image", "id_no", "phone", "selfie_image"]
        self.check_required_data(required_data, body)

        response = self.send_request("POST", "card-users/create", json=body)
        return self.__generate_cardUser_object(data=response.get("data", {}).get("cardUser"))

    def list_card_user(self, **kwargs):
        """
            list all card user
            GET request
        """
        url_params = None
        if kwargs != {}:
            url_params = pagination_filter(**kwargs)
        response = self.send_request("GET", f"card-users?{url_params}")
        data = response["data"]
        return [self.__generate_cardUser_object(cardUser_data) for cardUser_data in data]

    def show_card_user(self, reference):
        """
            show card user details
            GET request
        """
        response = self.send_request("GET", f"card-users/{reference}")
        return self.__generate_cardUser_object(data=response.get("data", {}).get("cardUser"))
