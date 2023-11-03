from typing import Optional

from swh.graphql.server import get_config

from .base_node import BaseNode
from .content import BaseContentNode


class ContentDataNode(BaseNode):
    obj: BaseContentNode

    @property
    def url(self) -> str:
        content_sha1 = self.obj.hashes["sha1"]
        archive_url = "https://archive.softwareheritage.org/api/1/"
        return f"{archive_url}content/sha1:{content_sha1}/raw/"

    @property
    def raw(self) -> Optional[bytes]:
        # Return content data as a binary string
        if self.obj.length <= get_config().get("max_raw_content_size", 10000):
            content_sha1 = self.obj.hashes["sha1"]
            return self.archive.get_content_data(content_sha1=content_sha1)
        return None

    def _get_node_data(self):
        # No new data to fetch: everything is either available
        # or can be computed from the parent (self.obj)
        # raw data is fetched from a property to avoid pre-loading
        return {}
