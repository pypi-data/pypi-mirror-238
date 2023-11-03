# Copyright (C) 2022 The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from swh.graphql.errors import DataError
from swh.graphql.utils import utils
from swh.model.model import ObjectType, Sha1Git

from .base_connection import BaseConnection, ConnectionData
from .base_node import BaseNode


class BaseDirectoryEntryNode(BaseNode):
    def target_hash(self) -> Sha1Git:
        assert self._node is not None
        return self._node.target

    def target_type(self) -> ObjectType:
        mapping = {
            "file": ObjectType.CONTENT,
            "dir": ObjectType.DIRECTORY,
            "rev": ObjectType.REVISION,
        }
        assert self._node is not None
        return mapping[self._node.type]


class DirectoryEntryNode(BaseDirectoryEntryNode):
    """
    Node resolver for a directory entry requested with a
    directory SWHID and a relative path
    """

    def _get_node_data(self):
        # STORAGE-TODO, archive is returning a dict
        # return DirectoryEntry object instead
        return self.archive.get_directory_entry_by_path(
            directory_id=self.kwargs.get("directorySWHID").object_id,
            path=self.kwargs.get("path"),
        )


class DirectoryEntryConnection(BaseConnection):
    """
    Connection resolver for entries in a directory
    """

    from .directory import BaseDirectoryNode

    obj: BaseDirectoryNode

    _node_class = BaseDirectoryEntryNode

    def _name_filter(self, dir_entry_name, name_include):
        if not self.kwargs.get("caseSensitive", False):
            return name_include.casefold() in dir_entry_name.decode().casefold()
        return name_include in dir_entry_name.decode()

    def _get_connection_data(self) -> ConnectionData:
        # FIXME, using dummy(local) pagination, move pagination to backend
        # STORAGE-TODO
        response = self.archive.get_directory_entries(self.obj.swhid.object_id)
        if response is None:
            # directory must be available in this case as it is a reference
            raise DataError("Directory object is missing on entries")
        entries = response.results
        if self.kwargs.get("nameInclude") is not None:
            # STORAGE-TODO, move this filter to swh-storage
            entries = [
                entry
                for entry in entries
                if self._name_filter(entry.name, self.kwargs.get("nameInclude"))
            ]
        return utils.get_local_paginated_data(
            entries, self._get_first_arg(), self._get_after_arg()
        )
