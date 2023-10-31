import requests
from requests.structures import CaseInsensitiveDict


class ReachApiGateway:
    def __init__(self, base_url, access_token):
        self.base_url = base_url
        self.headers = CaseInsensitiveDict(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "authorization": f"Bearer {access_token}",
            }
        )

    def review_profile_patch_business(self, business_id):
        resp = requests.patch(
            f"{self.base_url}/review-profile/business/{business_id}",
            headers=self.headers,
        )
        return resp
