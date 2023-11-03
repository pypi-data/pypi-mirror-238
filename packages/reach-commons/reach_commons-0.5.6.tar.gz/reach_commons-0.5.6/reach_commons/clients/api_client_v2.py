import requests
from requests.structures import CaseInsensitiveDict


class ReachApiGatewayV2:
    def __init__(self, base_url, access_token):
        self.base_url = base_url
        self.headers = CaseInsensitiveDict(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "authorization": f"Bearer {access_token}",
            }
        )

    def stripe_create_subscription(self, user_id, business_id):
        resp = requests.post(
            f"{self.base_url}/stripe/user/{user_id}/business/{business_id}/subscription",
            headers=self.headers,
        )
        return resp

    def stripe_create_customer(self, user_id):
        resp = requests.post(
            f"{self.base_url}/stripe/user/{user_id}/customer",
            headers=self.headers,
        )
        return resp

    def stripe_create_booking_guarantee(self, business_id, booking_price):
        resp = requests.post(
            f"{self.base_url}/stripe/business/{business_id}/booking-guarantee/",
            headers=self.headers,
            params={"booking_price": booking_price},
        )
        return resp

    def stripe_get_customer(self, user_id):
        resp = requests.get(
            f"{self.base_url}/stripe/user/{user_id}/customer", headers=self.headers
        )
        return resp

    def stripe_get_cards(self, user_id):
        resp = requests.get(
            f"{self.base_url}/stripe/user/{user_id}/cards", headers=self.headers
        )
        return resp

    def stripe_set_default_payment_method(self, user_id: int, default_payment_method):
        resp = requests.patch(
            f"{self.base_url}/stripe/user/{user_id}/default_payment/{default_payment_method}",
            headers=self.headers,
        )
        return resp

    def stripe_create_setup_intent(self, user_id: int):
        resp = requests.post(
            f"{self.base_url}/stripe/user/{user_id}/setup_intent", headers=self.headers
        )
        return resp

    def stripe_delete_payment_method(self, payment_method: str):
        resp = requests.delete(
            f"{self.base_url}/stripe/payment_method/{payment_method}",
            headers=self.headers,
        )
        return resp

    def stripe_cancel_subscription(self, business_id: int):
        resp = requests.delete(
            f"{self.base_url}/stripe/business/{business_id}", headers=self.headers
        )
        return resp


#
# api_gateway = ReachApiGatewayV2(
#     base_url="https://api-staging.getreach.ai",
#     access_token="6c6adc18-22a9-929f-648d-786eb20ebcf4",
# )
# stripe_customer = api_gateway.stripe_create_customer(
#     user_id=1,
#     description="wilson",
#     name="teste",
#     email="teste@gmail.com",
#     phone=None,
# )
