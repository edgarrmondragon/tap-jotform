"""REST client handling, including JotformStream base class."""

from typing import Any, Dict, Optional

import requests
import requests_cache
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.streams import RESTStream
from structlog.contextvars import bind_contextvars

requests_cache.install_cache("requests_cache")


class JotformStream(RESTStream):
    """Jotform stream class."""

    page_size = 100
    primary_keys = ["id"]
    records_jsonpath = "$.content[*]"

    INTEGER_FIELDS = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bind_contextvars(stream=self.name)

    def _sync_records(self, context: Optional[dict] = None) -> None:
        bind_contextvars(context=context)
        return super()._sync_records(context=context)

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

    def parse_response(self, response: requests.Response):
        self.logger.info("Received response", limit_left=response.json()["limit-left"])
        yield from super().parse_response(response)


class JotformPaginatedStream(JotformStream):
    """A Jotform stream with pagination."""

    replication_key = "updated_at"

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
        params = {"limit": self.page_size}

        starting_value = self.get_starting_timestamp(context)
        if starting_value:
            self.logger.info("Bookmark found", bookmark=starting_value)
            params["filter"] = f'{{"{self.replication_key}:gt": "{starting_value}"}}'

        if next_page_token:
            params["offset"] = next_page_token
        self.logger.info("Params", params=params)

        return params

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        row = super().post_process(row, context)
        row["updated_at"] = row["updated_at"] or row["created_at"]
        return row
