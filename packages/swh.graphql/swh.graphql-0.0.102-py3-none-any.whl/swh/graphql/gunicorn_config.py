# Copyright (C) 2023  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from graphql import GraphQLError, GraphQLSyntaxError
from sentry_sdk.integrations.ariadne import AriadneIntegration

from swh.core.sentry import init_sentry
from swh.graphql.errors import InvalidInputError, ObjectNotFoundError, PaginationError


def skip_expected_errors(event, hint):
    if "exc_info" in hint:
        _, exc_value, _ = hint["exc_info"]
        expected_errors = (
            ObjectNotFoundError,
            PaginationError,
            InvalidInputError,
            GraphQLError,
        )
        # GraphQLError is included to avoid an ariadne bug that
        # raises two errors for a scalar validation
        if isinstance(exc_value, GraphQLError) and isinstance(
            exc_value.original_error, expected_errors
        ):
            return None
        expected_base_errors = (
            GraphQLSyntaxError,
            GraphQLError,
        )  # A query syntax or a validation error
        if (
            isinstance(exc_value, expected_base_errors)
            and exc_value.original_error is None
        ):
            return None
    # a crash, send to sentry as unhandled
    return event


def post_fork(server, worker):
    init_sentry(
        sentry_dsn=None,  # set through SWH_SENTRY_DSN environment variable
        integrations=[AriadneIntegration()],
        extra_kwargs={
            # required to include GraphQL requests and responses data in sentry reports
            "send_default_pii": True,
            "before_send": skip_expected_errors,
        },
    )
