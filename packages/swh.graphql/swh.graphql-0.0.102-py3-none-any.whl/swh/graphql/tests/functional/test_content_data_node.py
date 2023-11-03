import base64

from . import utils
from ..data import get_contents, get_too_big_contents


def test_content_raw_data(client, mocker):
    content = get_contents()[0]
    # this patch is to skip using obj-storage
    mocker.patch(
        "swh.storage.objstorage.ObjStorage.content_get",
        return_value=content.data,
    )
    query_str = """
    query getContents($swhid: SWHID!) {
      contentsBySWHID(swhid: $swhid) {
        data {
          url
          raw {
            text
            base64
          }
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str, swhid=str(content.swhid()))
    archive_url = "https://archive.softwareheritage.org/api/1/"
    assert data["contentsBySWHID"][0] == {
        "data": {
            "url": f"{archive_url}content/sha1:{content.sha1.hex()}/raw/",
            "raw": {
                "text": content.data.decode(),
                "base64": base64.b64encode(content.data).decode("ascii"),
            },
        }
    }


def test_content_raw_data_too_long_content(client, mocker):
    content = get_too_big_contents()[0]
    mocker.patch(
        "swh.storage.objstorage.ObjStorage.content_get",
        return_value=content.data,
    )
    query_str = """
    query getContents($swhid: SWHID!) {
      contentsBySWHID(swhid: $swhid) {
        data {
          raw {
            text
            base64
          }
        }
      }
    }
    """
    data, _ = utils.get_query_response(client, query_str, swhid=str(content.swhid()))
    assert data["contentsBySWHID"][0] == {"data": {"raw": None}}
