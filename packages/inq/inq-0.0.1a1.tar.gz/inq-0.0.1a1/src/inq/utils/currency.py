import re

import requests

BASE_URL = \
    "https://api.rates-history-service.prd.aws.ofx.com/rate-history/api/1"


class CurrencyConverter:
    arg_pattern = re.compile(
        r"(?P<amount>\d+(:?.\d{1,2})?)\s*(?P<from>\w+) to (?P<to>\w+)"
    )

    def __init__(self, amount: float, from_currency: str, to_currency: str):
        self.amount = amount
        self.from_currency = from_currency.upper()
        self.to_currency = to_currency.upper()

    @classmethod
    def from_match(cls, match: re.Match):
        groups = match.groupdict()
        return cls(float(groups["amount"]), groups["from"], groups["to"])

    def run(self):
        return self.current_rate() * self.amount

    def current_rate(self):
        response = requests.post(
            BASE_URL,
            json={
                "method": "spotRateHistory",
                "data": {
                    "base": self.from_currency,
                    "term": self.to_currency,
                }
            }
        )
        response.raise_for_status()
        return response.json()["data"]["CurrentInterbankRate"]
