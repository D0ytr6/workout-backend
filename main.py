import uvicorn
from fastapi import FastAPI, APIRouter

from api.handlers import user_router
from db.session import init_db

# create instance of the app
app = FastAPI(title="workout-backend-app")


# create tables in async mode
# @app.on_event("startup")
# async def on_startup():
#     await init_db()
#

# create the instance for the routes
main_api_router = APIRouter()

# set routes to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)

if __name__ == "__main__":
    # run app on the host and port
    uvicorn.run(app, host="127.0.0.1", port=8000)
