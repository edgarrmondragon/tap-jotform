"""Jotform tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th
from singer_sdk.helpers._compat import metadata

from tap_jotform.streams import FormsStream, QuestionsForms, SubmissionsStream

STREAM_TYPES = [
    FormsStream,
    QuestionsForms,
    SubmissionsStream,
]

TAP_NAME = "tap-jotform"

USER_AGENT_SETTING = th.Property(
    "user_agent",
    th.StringType,
    default=f"{TAP_NAME}/{metadata.version(TAP_NAME)}",
    description="User-Agent",
)


class TapJotform(Tap):
    """Singer Tap for Jotform."""

    name = TAP_NAME

    config_jsonschema = th.PropertiesList(
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
        USER_AGENT_SETTING,
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
