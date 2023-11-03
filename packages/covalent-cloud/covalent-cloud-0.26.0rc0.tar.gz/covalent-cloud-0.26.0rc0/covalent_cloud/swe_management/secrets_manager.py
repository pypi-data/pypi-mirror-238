# Copyright 2023 Agnostiq Inc.

from typing import Optional
from covalent_cloud import get_client
from covalent_cloud.shared.classes.settings import Settings, settings


def store_secret(name: str, value: str, settings: Optional[Settings] = settings):
    client = get_client(settings)
    body = {
        "name": name,
        "value": value,
    }
    r = client.post("/api/v2/secrets", request_options={"json": body})
    r.raise_for_status()


def list_secrets(settings: Optional[Settings] = settings):
    client = get_client(settings)
    r = client.get("/api/v2/secrets")
    r.raise_for_status()
    return r.json()["names"]


def delete_secret(name: str, settings: Optional[Settings] = settings):
    client = get_client(settings)

    r = client.delete(f"/api/v2/secrets/{name}")
    r.raise_for_status()
