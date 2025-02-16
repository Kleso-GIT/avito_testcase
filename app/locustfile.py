import random
from locust import HttpUser, task, between

BASE_URL = "http://localhost:8000"


class FastApiUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.token = self.login()

    def login(self):
        response = self.client.post(
            "/api/auth",
            data={
                "username": "testuser2",
                "password": "testpassword2"
            }
        )
        return response.json().get("token")

    @task
    def send_coin(self):
        send_data = {
            "toUser": "string",
            "amount": random.randint(1, 2)
        }
        self.client.post(
            "/api/sendCoin",
            json=send_data,
            headers={"Authorization": f"Bearer {self.token}"},
        )

    @task
    def get_user_info(self):
        self.client.get(
            "/api/info",
            headers={"Authorization": f"Bearer {self.token}"},
        )

    @task
    def buy_item(self):
        item = random.choice(["cup", "book", "pen"])
        self.client.get(
            f"/api/buy/{item}",
            headers={"Authorization": f"Bearer {self.token}"},
        )
