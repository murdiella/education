import requests


class UniversityAdapter:
    def __init__(
        self,
        user,
        password,
        host,
        infobase,
        port,
        protocol,
    ):
        self.session = requests.Session()
        self.session.auth = (
            user,
            password,
        )
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Connection": "keep-alive",
            }
        )
        self.url = self.create_url(
            host=host,
            infobase=infobase,
            protocol=protocol,
            port=port,
        )

    @staticmethod
    def create_url(
        host,
        infobase,
        protocol="https",
        port=None,
    ):
        port_postfix = "" if not port else f":{port}"
        return f"{protocol}://{host}{port_postfix}/{infobase}/odata/standard.odata/"

    def create_resource_url(self, adapter):
        resource_name = f"Catalog_{adapter}"
        fields = None
        select = "*"
        if fields is not None:
            select = ",".join(fields)
        # TODO fix url construction
        return f"{self.url}{resource_name}?$select={select}"

    def get(self, adapter):
        url = self.create_resource_url(adapter)
        response = self.session.get(url)
        return response.json()["value"]

    def pull(self, target):
        items = self.get(target)
        return items
