from fastapi import FastAPI
import uvicorn
from routes.index import router
from schedule.image_scheduler import start_scheduler

app = FastAPI()

app.include_router(router)

start_scheduler()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
