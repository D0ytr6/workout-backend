"""File with settings and configs for the project"""

from envparse import Env

env = Env()

# asyncpg - async connect
# psycopg - sync connect

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://user:1234@127.0.0.1:5432/workoutDB"
)  # connect string for the database
