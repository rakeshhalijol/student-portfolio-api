from .connection import (
    connect,
    create_database
)

client = connect("mongodb://localhost:27017")
db = create_database(client=client, db_name="TEST-DATABASE")


# --- Create your collections here ---
User = db["User"]

# Write functions which interact with database


def create_user(userData: dict) -> str:
    user = User.insert_one(userData)
    return str(user.inserted_id)
