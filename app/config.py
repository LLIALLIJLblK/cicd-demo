import os
from typing import Optional

class Settings:
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'postgres')}@db:5432/myapp"
    )
    TEST_DATABASE_URL: str = os.getenv(
        "TEST_DATABASE_URL", 
        f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'postgres')}@localhost:5436/test_db"
    )

settings = Settings()