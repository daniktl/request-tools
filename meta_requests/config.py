import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    allow_insecure_connections = False
    certs_path = os.getenv("certs_path")
