from .connection import (
    connect,
    create_database
)

from src.config import (
    MONGODB_URL,
    DATABASE_NAME
)

client = connect(MONGODB_URL)
db = create_database(client=client, db_name=DATABASE_NAME)


# --- Create your collections here ---
User = db["User"]

# Write functions which interact with database


def create_user(userData: dict) -> str:
    user = User.insert_one(userData)
    return str(user.inserted_id)
