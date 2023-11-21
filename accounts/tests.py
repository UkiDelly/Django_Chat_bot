from django.test import TestCase, Client


# Create your tests here.
class AccountAPITest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()

    def test_register(self):
        data = {"nickname": "test", "email": "test@test.com", "password": "wjdrmsdud0922", "sns_id": "123",
                "social_type": "email"}

        res = self.client.post("/accounts/register/", data, content_type="application/json")
        print(res)
