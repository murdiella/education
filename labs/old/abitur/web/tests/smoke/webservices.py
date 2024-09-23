import requests
import os


def smoke_test_webservices():
    session = requests.Session()

    user = os.getenv("WSDL_USER")
    password = os.getenv("WSDL_PASSWORD")
    url = os.getenv("WSDL_URL")

    session.auth = (
        user,
        password,
    )
    response = session.get(url)
    assert response.status_code == 200
