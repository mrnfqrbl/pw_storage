import uvicorn
from fastapi import FastAPI, APIRouter
from starlette.staticfiles import StaticFiles

app=FastAPI()
api=APIRouter()

api.mount("/web",StaticFiles(directory="web"),name="static")
app.include_router(api)


uvicorn.run(app,host="127.0.0.1",port=8000)