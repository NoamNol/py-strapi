from enum import Enum


class PublicationState(str, Enum):
    live = "live"
    """returns only published entries (default)"""
    preview = "preview"
    """returns both draft entries & published entries"""
