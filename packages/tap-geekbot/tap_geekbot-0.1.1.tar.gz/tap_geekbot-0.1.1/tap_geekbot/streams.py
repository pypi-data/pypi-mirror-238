"""Stream type classes for tap-geekbot."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th

from tap_geekbot.client import GeekbotStream

user = th.ObjectType(
    th.Property("id", th.StringType),
    th.Property("email", th.EmailType),
    th.Property("username", th.StringType),
    th.Property("realname", th.StringType),
    th.Property("profile_img", th.StringType),
)

question = th.ObjectType(
    th.Property("id", th.IntegerType),
    th.Property("color", th.StringType),
    th.Property("text", th.StringType),
    th.Property("schedule", th.StringType),
    th.Property("answer_type", th.StringType),
    th.Property("answer_choices", th.ArrayType(th.StringType)),
    th.Property("hasAnswers", th.BooleanType),
    th.Property("is_random", th.BooleanType),
    th.Property("random_texts", th.ArrayType(th.StringType)),
    th.Property("prefilled_by", th.IntegerType),
    th.Property("text_id", th.IntegerType),
    th.Property("preconditions", th.ArrayType(th.StringType)),
    th.Property("label", th.StringType),
)


class Teams(GeekbotStream):
    """Teams stream."""

    name = "teams"
    path = "/v1/teams"
    records_jsonpath = "$.users[*]"

    schema = user.to_dict()


class Reports(GeekbotStream):
    """Reports stream."""

    name = "reports"
    path = "/v1/reports"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("slack_ts", th.StringType),
        th.Property("standup_id", th.IntegerType),
        th.Property("timestamp", th.IntegerType),
        th.Property("channel", th.StringType),
        th.Property("is_anonymous", th.BooleanType),
        th.Property("is_confidential", th.BooleanType),
        th.Property("members", th.ArrayType(user)),
        th.Property(
            "questions",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property("question", th.StringType),
                    th.Property("question_id", th.IntegerType),
                    th.Property("color", th.StringType),
                    th.Property("answer", th.StringType),
                    th.Property("images", th.ArrayType(th.StringType)),
                ),
            ),
        ),
    ).to_dict()

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: t.Any | None,  # noqa: ANN401
    ) -> dict[str, t.Any]:
        """Return the URL params for the request."""
        params = super().get_url_params(context, next_page_token)
        params["limit"] = 100
        return params


class StandUps(GeekbotStream):
    """Reports stream."""

    name = "standups"
    path = "/v1/standups"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("time", th.TimeType),
        th.Property(
            "wait_time",
            th.NumberType,
            description=(
                "Minutes to wait after user logs in before asking question. "
                "Null value means no automated asking."
            ),
        ),
        th.Property("timezone", th.StringType),
        th.Property("days", th.ArrayType(th.StringType)),
        th.Property("channel", th.StringType),
        th.Property("channel_ready", th.BooleanType),
        th.Property("questions", th.ArrayType(question)),
        th.Property("users", th.ArrayType(user)),
        th.Property("users_total", th.IntegerType),
        th.Property("webhooks", th.ArrayType(th.StringType)),
        th.Property("master", th.StringType),
        th.Property("sync_channel_members", th.BooleanType),
    ).to_dict()
