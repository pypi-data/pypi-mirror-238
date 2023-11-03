# Copyright (C) 2023 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import pytest

from swh.graphql.resolvers.base_node import BaseNode


class TestBaseNode:
    @pytest.fixture
    def dummy_node(self):
        class DummyNode(BaseNode):
            pass

        return DummyNode(obj=None, info=None, node_data={"test": 1})

    def test_is_type_of(self, dummy_node):
        assert dummy_node.is_type_of() == "DummyNode"
