# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from typing import List, Optional, Tuple

from swh.model.model import CoreSWHID, SnapshotBranch
from swh.storage.interface import PagedResult

from .base_connection import BaseConnection, ConnectionData
from .base_node import BaseNode
from .snapshot import BaseSnapshotNode


class BaseSnapshotBranchNode(BaseNode):
    def _get_node_from_data(self, node_data: Tuple[bytes, Optional[SnapshotBranch]]):
        # node_data is a tuple as returned by _get_connection_data in SnapshotBranchConnection
        # overriding to support this special data structure
        branch_name, branch_obj = node_data
        updated_node_data = {
            # Name of the branch, exposed in the schema
            "name": branch_name,
            # Type of the branch, exposed in the schema
            "type": branch_obj.target_type.value if branch_obj else None,
            # not exposed in the schema, to be used by the target object
            "snapshot_id": self._get_snapshot_swhid().object_id,
            # not exposed in the schema, to be used by the target object
            "target": branch_obj,
        }
        return super()._get_node_from_data(updated_node_data)


class SnapshotBranchConnectionNode(BaseSnapshotBranchNode):
    """
    Node resolver for an item in the snapshot branch connection
    """

    obj: "SnapshotBranchConnection"

    def _get_snapshot_swhid(self) -> CoreSWHID:
        # As of now parent of a SnapshotBranchConnection will always be a snapshot object
        # so, self.obj.obj will always be a BaseSnapshot object
        assert isinstance(self.obj.obj, BaseSnapshotNode)
        return self.obj.obj.swhid


class SnapshotHeadBranchNode(BaseSnapshotBranchNode):
    """
    Node resolver for a snapshot.headBranch object
    """

    obj: BaseSnapshotNode

    _can_be_null = True

    def _get_node_data(self) -> Optional[Tuple[bytes, Optional[SnapshotBranch]]]:
        snapshot_id = self._get_snapshot_swhid().object_id
        name = b"HEAD"
        # Get just the branch without following the alias chain
        # final target will be resolved only on requesting the target
        head_branch = self.archive.get_branch_by_name(
            snapshot_id=snapshot_id, branch_name=name, follow_chain=False
        )
        if head_branch is None or head_branch.branch_found is False:
            return None
        return (name, head_branch.target)

    def _get_snapshot_swhid(self) -> CoreSWHID:
        return self.obj.swhid


class SnapshotBranchConnection(BaseConnection):
    """
    Connection resolver for the branches in a snapshot
    """

    obj: BaseSnapshotNode

    _node_class = SnapshotBranchConnectionNode

    def _get_connection_data(self) -> ConnectionData:
        branches = self.archive.get_snapshot_branches(
            snapshot=self.obj.swhid.object_id,
            after=self._get_after_arg(),
            first=self._get_first_arg(),
            target_types=self.kwargs.get("types"),
            name_include=self._get_name_include_arg(),
            name_exclude_prefix=self._get_name_exclude_prefix_arg(),
        )
        end_cursor: Optional[bytes] = branches.get("next_branch") if branches else None
        # FIXME, this pagination is not consistent with other connections
        # FIX in swh-storage to return PagedResult
        # STORAGE-TODO

        # each result item will be converted to a dict in _get_node_from_data
        # method in the node class
        results: List[Tuple[bytes, Optional[SnapshotBranch]]] = (
            list(branches["branches"].items()) if branches else []
        )
        return ConnectionData(
            paged_result=PagedResult(
                results=results,
                next_page_token=end_cursor.decode() if end_cursor else None,
            )
        )

    def _get_after_arg(self):
        # after argument must be an empty string by default
        after = super()._get_after_arg()
        return after.encode() if after else b""

    def _get_name_include_arg(self):
        name_include = self.kwargs.get("nameInclude", None)
        return name_include.encode() if name_include else None

    def _get_name_exclude_prefix_arg(self):
        name_exclude_prefix = self.kwargs.get("nameExcludePrefix", None)
        return name_exclude_prefix.encode() if name_exclude_prefix else None

    def _get_index_cursor(self, index: int, node: BaseSnapshotBranchNode):
        # Snapshot branch is using a different cursor, hence the override
        # No item cursor is provided in this case
        # FIXME: Return the right cursor when enabling index cursors
        return None
