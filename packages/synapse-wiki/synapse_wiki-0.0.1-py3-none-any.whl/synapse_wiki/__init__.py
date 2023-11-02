import os

api_key = os.environ.get("SYNAPSE_API_KEY")

__all__ = [
    "api_key",
]

from .api import (
    create_collection,
    list_collections,
    query,
)
