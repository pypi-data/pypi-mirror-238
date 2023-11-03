# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from graphql import GraphQLError

from swh.graphql import errors


def test_errors():
    err = errors.ObjectNotFoundError("test error")
    assert str(err) == "Object error: test error"

    err = errors.PaginationError("test error")
    assert str(err) == "Pagination error: test error"

    err = errors.InvalidInputError("test error")
    assert str(err) == "Input error: test error"


def test_format_error_with_debug():
    err = GraphQLError("test error")
    response = errors.format_error(err, debug=True)
    assert "extensions" in response


def test_format_error_without_debug():
    err = GraphQLError("test error")
    response = errors.format_error(err)
    assert "extensions" not in response
