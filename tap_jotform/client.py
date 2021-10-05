"""REST client handling, including JotformStream base class."""

from typing import Any, Dict, Optional

import requests
import requests_cache
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.streams import RESTStream

requests_cache.install_cache("requests_cache")


class JotformStream(RESTStream):
    """Jotform stream class."""

    page_size = 100
    primary_keys = ["id"]
    replication_key = "created_at"
    records_jsonpath = "$.content[*]"

    INTEGER_FIELDS = []

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["api_url"]

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object."""
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="APIKEY",
            value=self.config["api_key"],
            location="header",
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        for field in self.INTEGER_FIELDS:
            value = row.get(field)
            row[field] = int(value) if value else None
        return row


class JotformPaginatedStream(JotformStream):
    """A Jotform stream with pagination."""

    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: Optional[Any],
    ) -> int:
        """Return a token for identifying next page or None if no more pages."""
        current_offset = previous_token or 0

        result_set = response.json()["resultSet"]
        count = int(result_set["count"])

        if count == self.page_size:
            return current_offset + self.page_size

        return None

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[int]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        state = self.get_context_state(context)
        self.logger.info("STATE %s", state)
        params = {"limit": self.page_size}

        if next_page_token:
            params["offset"] = next_page_token

        return params
