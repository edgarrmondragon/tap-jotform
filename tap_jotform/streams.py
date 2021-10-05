"""Stream type classes for tap-jotform."""

import json
from typing import Dict, Optional

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_jotform.client import JotformPaginatedStream, JotformStream

CREATED_AT = th.Property("created_at", th.DateTimeType)
UPDATED_AT = th.Property("updated_at", th.DateTimeType)
STATUS = th.Property("status", th.StringType)


class FormsStream(JotformPaginatedStream):
    """Forms stream."""

    name = "forms"
    path = "/user/forms"

    INTEGER_FIELDS = [
        "height",
        "new",
        "count",
        "favorite",
        "archived",
    ]

    schema = th.PropertiesList(
        th.Property("id", th.StringType, description="The Form ID"),
        th.Property("username", th.StringType),
        th.Property("title", th.StringType),
        th.Property("height", th.IntegerType),
        th.Property("url", th.StringType),
        STATUS,
        CREATED_AT,
        UPDATED_AT,
        th.Property("last_submission", th.DateTimeType),
        th.Property(
            "new",
            th.IntegerType,
            description="Total number of unread submissions",
        ),
        th.Property(
            "count",
            th.IntegerType,
            description="Total number of submissions",
        ),
        th.Property("type", th.StringType),
        th.Property("favorite", th.IntegerType),
        th.Property("archived", th.IntegerType),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        return {"form_id": record["id"]}


class QuestionsForms(JotformStream):
    "Questions stream."

    name = "questions"
    path = "/form/{form_id}/questions"
    primary_keys = ["form_id", "qid"]
    replication_key = None
    records_jsonpath = "$.content.*"
    parent_stream_type = FormsStream

    INTEGER_FIELDS = [
        "order",
        "cols",
        "rows",
        "maxsize",
        "size",
        "scaleFrom",
        "stars",
    ]

    schema = th.PropertiesList(
        th.Property("qid", th.StringType, required=True, description="Question ID"),
        th.Property("form_id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("hint", th.StringType),
        th.Property("description", th.StringType),
        th.Property("order", th.IntegerType),
        th.Property("text", th.StringType, description="Question label"),
        th.Property(
            "type",
            th.StringType,
            required=True,
            description="Question type such as textbox or dropdown",
        ),
        th.Property("required", th.StringType),
        th.Property("readonly", th.StringType),
        th.Property("defaultValue", th.StringType),
        th.Property("autoFixed", th.StringType),
        th.Property("cols", th.IntegerType),
        th.Property("rows", th.IntegerType),
        th.Property("entryLimit", th.StringType),
        th.Property("entryLimitMin", th.StringType),
        th.Property("maxsize", th.IntegerType),
        th.Property("size", th.IntegerType),
        th.Property("mde", th.StringType),
        th.Property("wysiwyg", th.StringType),
        th.Property("hidden", th.StringType),
        th.Property("inputTextMask", th.StringType),
        th.Property("suffix", th.StringType),
        th.Property("validation", th.StringType),
        th.Property("labelAlign", th.StringType),
        th.Property("buttonAlign", th.StringType),
        th.Property("buttonStyle", th.StringType),
        th.Property("clear", th.StringType),
        th.Property("clearText", th.StringType),
        th.Property("encryptIcon", th.StringType),
        th.Property("print", th.StringType),
        th.Property("printText", th.StringType),
        th.Property("scaleFrom", th.IntegerType),
        th.Property("stars", th.IntegerType),
        th.Property("starStyle", th.StringType),
        th.Property("prettyFormat", th.StringType),
        th.Property("subLabel", th.StringType),
        th.Property("toText", th.StringType),
        th.Property("fromText", th.StringType),
    ).to_dict()


class SubmissionsStream(JotformPaginatedStream):
    """Submissions stream."""

    name = "submissions"
    path = "/form/{form_id}/submissions"
    parent_stream_type = FormsStream

    INTEGER_FIELDS = [
        "flag",
        "new",
    ]

    schema = th.PropertiesList(
        th.Property("id", th.StringType, description="The Submission ID"),
        th.Property("form_id", th.StringType),
        th.Property("ip", th.StringType),
        th.Property("flag", th.IntegerType),
        th.Property("notes", th.StringType),
        CREATED_AT,
        UPDATED_AT,
        STATUS,
        th.Property(
            "new",
            th.IntegerType,
            description="Total number of unread submissions",
        ),
        th.Property(
            "answers",
            th.ArrayType(
                th.ObjectType(
                    th.Property("qid", th.StringType, required=True),
                    th.Property("answer", th.StringType),
                )
            ),
        ),
    ).to_dict()

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        row = super().post_process(row, context)

        answers_list = []
        answers: Dict[str, Dict[str, str]] = row.pop("answers", {})
        for qid, entry in answers.items():
            answer = entry.get("answer")
            entry["answer"] = json.dumps(answer) if answer is not None else None
            answers_list.append({"qid": qid, **entry})
        row["answers"] = answers_list

        return row
