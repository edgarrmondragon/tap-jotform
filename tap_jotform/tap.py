"""Jotform tap class."""

from typing import List

import structlog
from singer_sdk import Stream, Tap
from singer_sdk import typing as th
from singer_sdk.helpers._classproperty import classproperty
from structlog.contextvars import bind_contextvars, merge_contextvars

from tap_jotform.streams import FormsStream, QuestionsForms, SubmissionsStream

STREAM_TYPES = [
    FormsStream,
    QuestionsForms,
    SubmissionsStream,
]

structlog.configure(
    processors=[
        merge_contextvars,
        # structlog.processors.JSONRenderer(),
        structlog.dev.ConsoleRenderer(colors=True),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)


class TapJotform(Tap):
    """Singer Tap for Jotform."""

    name = "tap-jotform"

    @classproperty
    def logger(cls):
        bind_contextvars(tap=cls.name, version=cls.plugin_version)
        return structlog.get_logger()

    @classproperty
    def config_jsonschema(cls):
        return th.PropertiesList(
            th.Property(
                "api_url",
                th.StringType,
                required=False,
                default="https://api.jotform.com",
                description="The URL API",
            ),
            th.Property(
                "api_key",
                th.StringType,
                required=True,
                description="The token to authenticate against the API service",
            ),
            th.Property(
                "user_agent",
                th.StringType,
                default=f"{cls.name}/{cls.plugin_version}",
                description="User-Agent",
            ),
        ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
