"""Jotform tap class."""

from __future__ import annotations

from singer_sdk import Stream, Tap
from singer_sdk import typing as th
from singer_sdk.helpers._classproperty import classproperty

from tap_jotform import streams


class TapJotform(Tap):
    """Singer Tap for Jotform."""

    name = "tap-jotform"

    def get_user_agent(self) -> str:
        """Return a user agent string.

        Returns:
            A user agent string.
        """
        return f"{self.name}/{self.plugin_version}"

    @classproperty
    def config_jsonschema(cls) -> dict:  # type: ignore
        """Return the JSON schema definition for the config.

        Returns:
            The JSON schema definition for the config.
        """
        return th.PropertiesList(
            th.Property(
                "api_key",
                th.StringType,
                required=True,
                description=(
                    "Authentication key. "
                    "See https://api.jotform.com/docs/#authentication"
                ),
            ),
            th.Property(
                "api_url",
                th.StringType,
                required=False,
                default="https://api.jotform.com",
                description="API Base URL",
            ),
            th.Property(
                "user_agent",
                th.StringType,
                default=f"{cls.name}/{cls.plugin_version}",
                description="User-Agent header",
            ),
            th.Property(
                "start_date",
                th.DateTimeType,
                required=False,
                description="Start date for data collection",
            ),
            th.Property(
                "requests_cache",
                th.ObjectType(
                    th.Property(
                        "enabled",
                        th.BooleanType,
                        default=False,
                        description="Enable requests cache",
                    ),
                    th.Property(
                        "config",
                        th.ObjectType(
                            th.Property(
                                "expire_after",
                                th.IntegerType,
                                description="Cache expiration time in seconds",
                            ),
                        ),
                        description="Requests cache configuration",
                        default={},
                    ),
                ),
                description="Cache configuration for HTTP requests",
            ),
        ).to_dict()

    def discover_streams(self) -> list[Stream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.FormsStream(self),
            streams.QuestionsStream(self),
            streams.SubmissionsStream(self),
            streams.ReportsStream(self),
        ]
