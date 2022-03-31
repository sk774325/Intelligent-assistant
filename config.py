import os


class Config:
    """Service configurations"""
    HOST = os.environ.get("HOST", "140.116.154.113")
    PORT = int(os.environ.get("PORT", "8000"))

    FAKE_DATA = os.environ.get("FAKE_DATA", "false")