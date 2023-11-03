# Copyright (C) 2023 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from swh.graphql.resolvers.base_connection import (
    BaseConnection,
    BaseList,
    ConnectionData,
)
from swh.storage.interface import PagedResult


class TestBaseConnection:
    @pytest.fixture
    def dummy_connection(self):
        class DummyConnection(BaseConnection):
            def _get_connection_data(self):
                return ConnectionData(
                    paged_result=PagedResult(
                        results=[1, 2, 3, 4, 5],
                        next_page_token=None,
                    ),
                    total_count=5,
                )

        return DummyConnection(obj=None, info=None)

    def test_results(self, dummy_connection):
        nodes = dummy_connection.nodes
        page_info = dummy_connection.pageInfo
        assert nodes == [1, 2, 3, 4, 5]
        assert page_info.hasNextPage is False
        assert page_info.endCursor is None


class TestBaseList:
    @pytest.fixture
    def dummy_list(self):
        class DummyList(BaseList):
            def _get_results(self):
                return [1, 2, 3, 4, 5]

        return DummyList(obj=None, info=None)

    def test_results(self, dummy_list):
        assert dummy_list.get_results() == [1, 2, 3, 4, 5]
