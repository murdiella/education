import requests
import os


def smoke_test_odata_service():
    session = requests.session()
    protocol = os.getenv("ODATA_PROTOCOL")
    host = os.getenv("ODATA_HOST")
    port = os.getenv("ODATA_PORT")
    infobase = os.getenv("ODATA_INFOBASE")
    user = os.getenv("ODATA_USER")
    password = os.getenv("ODATA_PASSWORD")
    session.auth = (
        user,
        password,
    )
    port_postfix = "" if not port else f":{port}"
    url = f"{protocol}://{host}{port_postfix}/{infobase}/odata/standard.odata/"
    response = session.get(url)
    assert response.status_code == 200
