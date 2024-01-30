"""File with settings and configs for the project"""

from envparse import Env

env = Env()

# asyncpg - async connect
# psycopg - sync connect

ACCESS_TOKEN_EXPIRE_MINUTES: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES", default=30)
ACCESS_TOKEN_EXPIRE_MINUTES_TEST: int = env.int("ACCESS_TOKEN_EXPIRE_MINUTES_TEST", default=1)

REFRESH_TOKEN_EXPIRE_MINUTES: int = env.int("REFRESH_TOKEN_EXPIRE_MINUTES", default=(60 * 24 * 60))  # 2 months

SECRET_KEY: str = env.str("SECRET_KEY", default="MIICWwIBAAKBgQCCv1TjWeV8x1B9B6OuzNWQmcGftQ3iGnhpKNDpO4bvJjyCFOta")

ALGORITHM: str = env.str("ALGORITHM", default="HS256")

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default="postgresql+asyncpg://user:1234@127.0.0.1:5432/workoutDB"
)  # connect string for the database
