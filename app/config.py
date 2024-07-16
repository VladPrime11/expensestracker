import os
import secrets
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
        if not os.getenv("SECRET_KEY"):
            with open('.env', 'a') as f:
                f.write(f'SECRET_KEY={self.SECRET_KEY}\n')

config = Config()
