# Copyright 2023 Agnostiq Inc.


from typing import Optional
from covalent_cloud.shared.classes.settings import Settings, settings
from covalent_cloud import get_client


def volume(path: str, settings: Optional[Settings] = settings):
    """Return the persistent volume in the file system containing path

    :param path: path to a directory
    :return: volume id of the file system containing path
    """

    if (not path or not path.isalnum()):
        raise ValueError("Invalid path specified")

    client = get_client(settings)

    response = client.post(
        "/api/v2/volumes",
        request_options={"data": {"name": path}}
    )

    data = response.json()

    return data['id']
