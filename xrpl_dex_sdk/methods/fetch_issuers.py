from ..models.methods.fetch_issuers import FetchIssuersResponse


def fetch_issuers(self) -> FetchIssuersResponse:
    return self.load_data("issuers.json")
