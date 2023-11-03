# Copyright (C) 2023  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import os

from graphql import GraphQLError, GraphQLSyntaxError
import pytest

from swh.graphql import errors
import swh.graphql.gunicorn_config as gunicorn_config


def test_post_fork_default(mocker):
    sentry_sdk_init = mocker.patch("sentry_sdk.init")

    gunicorn_config.post_fork(None, None)

    sentry_sdk_init.assert_not_called()


def test_post_fork_with_dsn_env(mocker):
    ariadne_integration = object()  # unique object to check for equality
    mocker.patch(
        "swh.graphql.gunicorn_config.AriadneIntegration",
        new=lambda: ariadne_integration,
    )
    sentry_sdk_init = mocker.patch("sentry_sdk.init")
    mocker.patch.dict(os.environ, {"SWH_SENTRY_DSN": "test_dsn"})

    gunicorn_config.post_fork(None, None)

    sentry_sdk_init.assert_called_once_with(
        dsn="test_dsn",
        environment=None,
        integrations=[ariadne_integration],
        debug=False,
        release=None,
        send_default_pii=True,
        before_send=gunicorn_config.skip_expected_errors,
    )


def test_post_fork_debug(mocker):
    ariadne_integration = object()  # unique object to check for equality
    mocker.patch(
        "swh.graphql.gunicorn_config.AriadneIntegration",
        new=lambda: ariadne_integration,
    )
    sentry_sdk_init = mocker.patch("sentry_sdk.init")
    mocker.patch.dict(
        os.environ, {"SWH_SENTRY_DSN": "test_dsn", "SWH_SENTRY_DEBUG": "1"}
    )

    gunicorn_config.post_fork(None, None)

    sentry_sdk_init.assert_called_once_with(
        dsn="test_dsn",
        environment=None,
        integrations=[ariadne_integration],
        debug=True,
        release=None,
        send_default_pii=True,
        before_send=gunicorn_config.skip_expected_errors,
    )


@pytest.mark.parametrize(
    ("error, sent_to_sentry"),
    [
        (errors.ObjectNotFoundError("test"), False),
        (errors.PaginationError("test"), False),
        (errors.InvalidInputError("test"), False),
        (GraphQLError(None), False),  # type: ignore
        (NameError, True),  # Unhandled wrapped error
    ],
)
def test_skip_expected_errors(error, sent_to_sentry):
    event = {"test": "test-event"}
    err = GraphQLError("test error")
    err.original_error = error
    hint = {"exc_info": ("info", err, "traceback")}
    response = gunicorn_config.skip_expected_errors(event, hint)
    if sent_to_sentry:
        assert response == event
    else:
        assert response is None


@pytest.mark.parametrize(
    ("error, sent_to_sentry"),
    [
        (GraphQLSyntaxError(None, None, None), False),  # type: ignore
        (GraphQLError(None), False),  # type: ignore
        (NameError("test"), True),
    ],
)
def test_skip_base_errors(error, sent_to_sentry):
    event = {"test": "test-event"}
    hint = {"exc_info": ("info", error, "traceback")}
    response = gunicorn_config.skip_expected_errors(event, hint)
    if sent_to_sentry:
        assert response == event
    else:
        assert response is None
