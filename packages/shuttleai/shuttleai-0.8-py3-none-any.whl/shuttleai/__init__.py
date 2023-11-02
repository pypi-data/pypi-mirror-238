from .shuttleai import ShuttleClient
import os

api_key = os.environ.get("SHUTTLE_API_KEY")

__all__ = ['ShuttleClient']